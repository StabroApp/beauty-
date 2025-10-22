"""
Google Cloud Storage Utility Module

Handles data persistence operations with Google Cloud Storage.
Designed to work efficiently with the free tier (5GB regional storage).
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Union, TYPE_CHECKING
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from google.cloud import storage
    from google.cloud.exceptions import NotFound, GoogleCloudError
    GCS_AVAILABLE = True
except ImportError:
    logger.warning("google-cloud-storage not installed. GCS features will be disabled.")
    GCS_AVAILABLE = False
    # Create dummy types for type hints when not installed
    if TYPE_CHECKING:
        from google.cloud import storage


class GCSStorage:
    """Google Cloud Storage manager for beauty clinic data"""
    
    def __init__(self, bucket_name: Optional[str] = None, project_id: Optional[str] = None):
        """
        Initialize GCS Storage client
        
        Args:
            bucket_name: Name of the GCS bucket (defaults to env var GCS_BUCKET_NAME)
            project_id: GCP project ID (defaults to env var GCP_PROJECT_ID)
        """
        if not GCS_AVAILABLE:
            raise ImportError(
                "google-cloud-storage is not installed. "
                "Install it with: pip install google-cloud-storage"
            )
        
        self.bucket_name = bucket_name or os.getenv('GCS_BUCKET_NAME')
        self.project_id = project_id or os.getenv('GCP_PROJECT_ID')
        
        if not self.bucket_name:
            raise ValueError(
                "Bucket name not provided. Set GCS_BUCKET_NAME environment variable "
                "or pass bucket_name parameter."
            )
        
        try:
            self.client = storage.Client(project=self.project_id)
            self.bucket = self._get_or_create_bucket()
            logger.info(f"Successfully connected to GCS bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GCS client: {e}")
            raise
    
    def _get_or_create_bucket(self):
        """
        Get existing bucket or create a new one if it doesn't exist
        
        Returns:
            Google Cloud Storage bucket object
        """
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            logger.info(f"Found existing bucket: {self.bucket_name}")
            return bucket
        except NotFound:
            logger.info(f"Bucket {self.bucket_name} not found. Creating new bucket...")
            try:
                # Create bucket in a free tier eligible region
                # us-east1, us-west1, us-central1 are good choices for free tier
                bucket = self.client.create_bucket(
                    self.bucket_name,
                    location=os.getenv('GCS_LOCATION', 'us-east1')
                )
                logger.info(f"Successfully created bucket: {self.bucket_name}")
                return bucket
            except GoogleCloudError as e:
                logger.error(f"Failed to create bucket: {e}")
                raise
    
    def upload_json(
        self, 
        data: Union[List[Dict], Dict], 
        filename: str,
        folder: str = "clinics"
    ) -> str:
        """
        Upload JSON data to Cloud Storage
        
        Args:
            data: Data to upload (list or dict)
            filename: Name of the file
            folder: Folder path within the bucket (default: "clinics")
            
        Returns:
            GCS blob path (gs://bucket/folder/filename)
        """
        try:
            # Ensure filename has .json extension
            if not filename.endswith('.json'):
                filename = f"{filename}.json"
            
            blob_path = f"{folder}/{filename}" if folder else filename
            blob = self.bucket.blob(blob_path)
            
            # Convert data to JSON string
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            # Upload with metadata
            blob.upload_from_string(
                json_data,
                content_type='application/json'
            )
            
            # Set metadata
            blob.metadata = {
                'uploaded_at': datetime.utcnow().isoformat(),
                'data_type': 'clinic_data',
                'record_count': str(len(data) if isinstance(data, list) else 1)
            }
            blob.patch()
            
            gs_path = f"gs://{self.bucket_name}/{blob_path}"
            logger.info(f"Successfully uploaded {len(json_data)} bytes to {gs_path}")
            return gs_path
            
        except Exception as e:
            logger.error(f"Failed to upload {filename}: {e}")
            raise
    
    def upload_file(
        self, 
        local_path: str, 
        destination_path: Optional[str] = None
    ) -> str:
        """
        Upload a local file to Cloud Storage
        
        Args:
            local_path: Path to local file
            destination_path: Destination path in GCS (defaults to basename of local_path)
            
        Returns:
            GCS blob path (gs://bucket/path)
        """
        try:
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"Local file not found: {local_path}")
            
            if destination_path is None:
                destination_path = os.path.basename(local_path)
            
            blob = self.bucket.blob(destination_path)
            
            # Determine content type
            content_type = 'application/json' if local_path.endswith('.json') else None
            
            blob.upload_from_filename(local_path, content_type=content_type)
            
            gs_path = f"gs://{self.bucket_name}/{destination_path}"
            logger.info(f"Successfully uploaded {local_path} to {gs_path}")
            return gs_path
            
        except Exception as e:
            logger.error(f"Failed to upload file {local_path}: {e}")
            raise
    
    def download_json(self, blob_path: str) -> Union[List[Dict], Dict]:
        """
        Download and parse JSON data from Cloud Storage
        
        Args:
            blob_path: Path to blob in GCS (without gs://bucket/ prefix)
            
        Returns:
            Parsed JSON data (list or dict)
        """
        try:
            blob = self.bucket.blob(blob_path)
            
            if not blob.exists():
                raise NotFound(f"Blob not found: {blob_path}")
            
            # Download as string and parse JSON
            json_string = blob.download_as_string()
            data = json.loads(json_string)
            
            logger.info(f"Successfully downloaded {blob_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to download {blob_path}: {e}")
            raise
    
    def download_file(self, blob_path: str, local_path: str) -> str:
        """
        Download a file from Cloud Storage to local filesystem
        
        Args:
            blob_path: Path to blob in GCS
            local_path: Local path to save the file
            
        Returns:
            Local file path
        """
        try:
            blob = self.bucket.blob(blob_path)
            
            if not blob.exists():
                raise NotFound(f"Blob not found: {blob_path}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            blob.download_to_filename(local_path)
            
            logger.info(f"Successfully downloaded {blob_path} to {local_path}")
            return local_path
            
        except Exception as e:
            logger.error(f"Failed to download file {blob_path}: {e}")
            raise
    
    def list_files(
        self, 
        prefix: Optional[str] = None,
        suffix: Optional[str] = None
    ) -> List[Dict[str, Union[str, int, datetime]]]:
        """
        List files in Cloud Storage bucket
        
        Args:
            prefix: Filter by prefix (folder path)
            suffix: Filter by suffix (file extension)
            
        Returns:
            List of file metadata dictionaries
        """
        try:
            blobs = self.bucket.list_blobs(prefix=prefix)
            
            files = []
            for blob in blobs:
                # Apply suffix filter if provided
                if suffix and not blob.name.endswith(suffix):
                    continue
                
                files.append({
                    'name': blob.name,
                    'size': blob.size,
                    'created': blob.time_created,
                    'updated': blob.updated,
                    'content_type': blob.content_type,
                    'gs_path': f"gs://{self.bucket_name}/{blob.name}"
                })
            
            logger.info(f"Found {len(files)} files with prefix='{prefix}', suffix='{suffix}'")
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise
    
    def delete_file(self, blob_path: str) -> bool:
        """
        Delete a file from Cloud Storage
        
        Args:
            blob_path: Path to blob in GCS
            
        Returns:
            True if deleted successfully
        """
        try:
            blob = self.bucket.blob(blob_path)
            
            if not blob.exists():
                logger.warning(f"Blob not found: {blob_path}")
                return False
            
            blob.delete()
            logger.info(f"Successfully deleted {blob_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete {blob_path}: {e}")
            raise
    
    def delete_old_files(
        self, 
        prefix: Optional[str] = None,
        days_old: int = 30
    ) -> int:
        """
        Delete files older than specified number of days
        
        Args:
            prefix: Filter by prefix (folder path)
            days_old: Delete files older than this many days
            
        Returns:
            Number of files deleted
        """
        try:
            from datetime import timezone, timedelta
            
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
            blobs = self.bucket.list_blobs(prefix=prefix)
            
            deleted_count = 0
            for blob in blobs:
                if blob.updated < cutoff_date:
                    blob.delete()
                    deleted_count += 1
                    logger.info(f"Deleted old file: {blob.name}")
            
            logger.info(f"Deleted {deleted_count} files older than {days_old} days")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to delete old files: {e}")
            raise
    
    def get_file_metadata(self, blob_path: str) -> Dict:
        """
        Get metadata for a specific file
        
        Args:
            blob_path: Path to blob in GCS
            
        Returns:
            Dictionary with file metadata
        """
        try:
            blob = self.bucket.blob(blob_path)
            
            if not blob.exists():
                raise NotFound(f"Blob not found: {blob_path}")
            
            # Reload to get latest metadata
            blob.reload()
            
            metadata = {
                'name': blob.name,
                'size': blob.size,
                'created': blob.time_created,
                'updated': blob.updated,
                'content_type': blob.content_type,
                'gs_path': f"gs://{self.bucket_name}/{blob.name}",
                'custom_metadata': blob.metadata or {}
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get metadata for {blob_path}: {e}")
            raise
    
    def get_bucket_info(self) -> Dict:
        """
        Get information about the storage bucket
        
        Returns:
            Dictionary with bucket information
        """
        try:
            # Reload bucket to get latest info
            self.bucket.reload()
            
            # Calculate total size
            total_size = 0
            file_count = 0
            for blob in self.bucket.list_blobs():
                total_size += blob.size or 0
                file_count += 1
            
            info = {
                'name': self.bucket.name,
                'location': self.bucket.location,
                'storage_class': self.bucket.storage_class,
                'created': self.bucket.time_created,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'file_count': file_count
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to get bucket info: {e}")
            raise


def main():
    """Example usage of GCS Storage"""
    # Check if GCS is available
    if not GCS_AVAILABLE:
        print("google-cloud-storage is not installed.")
        print("Install it with: pip install google-cloud-storage")
        return
    
    # Example configuration
    print("GCS Storage Example Usage")
    print("=" * 50)
    
    # Initialize storage (requires GCS_BUCKET_NAME environment variable)
    try:
        storage = GCSStorage()
        
        # Example 1: Upload JSON data
        sample_data = [
            {
                "id": "clinic_1",
                "name": "Sample Clinic",
                "rating": 4.5
            }
        ]
        
        print("\n1. Uploading sample data...")
        gs_path = storage.upload_json(sample_data, "sample_clinics.json")
        print(f"   Uploaded to: {gs_path}")
        
        # Example 2: List files
        print("\n2. Listing files...")
        files = storage.list_files(prefix="clinics", suffix=".json")
        for f in files[:5]:  # Show first 5
            print(f"   - {f['name']} ({f['size']} bytes)")
        
        # Example 3: Download data
        print("\n3. Downloading data...")
        data = storage.download_json("clinics/sample_clinics.json")
        print(f"   Downloaded {len(data)} records")
        
        # Example 4: Get bucket info
        print("\n4. Bucket information...")
        info = storage.get_bucket_info()
        print(f"   Bucket: {info['name']}")
        print(f"   Location: {info['location']}")
        print(f"   Total size: {info['total_size_mb']} MB")
        print(f"   File count: {info['file_count']}")
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nSet the following environment variables:")
        print("  - GCS_BUCKET_NAME: Your GCS bucket name")
        print("  - GCP_PROJECT_ID: Your GCP project ID (optional)")
        print("  - GOOGLE_APPLICATION_CREDENTIALS: Path to service account key (optional)")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
