# Contributing to PROJECT BEAUTY

Thank you for your interest in contributing to PROJECT BEAUTY! This guide will help you get started.

## How to Contribute

There are many ways to contribute to this project:

1. **Report Bugs** - Found a bug? Open an issue
2. **Suggest Features** - Have an idea? We'd love to hear it
3. **Improve Documentation** - Help make our docs clearer
4. **Write Code** - Submit pull requests to fix issues or add features
5. **Add Clinic Data** - Help expand our database of Japanese beauty clinics

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/beauty-.git
   cd beauty-
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Testing Your Changes

Before submitting a pull request, make sure to:

1. Run the test suite:
   ```bash
   python tests.py
   ```

2. Test the scraper:
   ```bash
   python scraper/hotpepper_scraper.py --location tokyo --category salon
   ```

3. Test the advisor:
   ```bash
   python beauty_advisor.py
   ```

4. Run the demo:
   ```bash
   python demo.py
   ```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Comment complex logic

## Areas for Contribution

### High Priority

- **Real Web Scraping**: Implement actual scraping from beauty.hotpepper.jp
- **Database Integration**: Replace JSON storage with proper database (SQLite, PostgreSQL)
- **User Interface**: Create a web interface using Flask or FastAPI
- **Authentication**: Add user accounts and saved searches
- **Reviews System**: Add ability to rate and review clinics

### Medium Priority

- **More Languages**: Add support for Chinese, Korean, Spanish
- **Mobile App**: Create a mobile application
- **Booking Integration**: Direct booking integration with clinics
- **Map Integration**: Add Google Maps or similar for clinic locations
- **Photo Gallery**: Add clinic photos and before/after images

### Low Priority

- **Social Features**: Share recommendations with friends
- **Notifications**: Alert users about new clinics or promotions
- **Analytics**: Track popular searches and clinics
- **Export Features**: Export clinic lists to PDF or CSV

## Adding New Features

When adding a new feature:

1. **Discuss First**: Open an issue to discuss major changes
2. **Keep it Small**: Make incremental, focused changes
3. **Write Tests**: Add tests for new functionality
4. **Update Docs**: Update README and USAGE.md as needed
5. **Add Examples**: Include usage examples in your PR

## Expanding the Scraper

To add support for new locations or categories:

1. Update `_generate_sample_data()` in `hotpepper_scraper.py`
2. Add the new location/category data
3. Test the scraper with the new options
4. Update documentation

For real scraping implementation:

1. Study the structure of beauty.hotpepper.jp
2. Implement respectful scraping (rate limiting, robots.txt)
3. Handle pagination and error cases
4. Parse HTML/JSON responses correctly
5. Store data in consistent format

## Improving the AI Advisor

To enhance the AI advisor:

1. Improve prompt engineering in `advisor_agent.py`
2. Add new conversation intents
3. Enhance the fallback responses
4. Add context management for multi-turn conversations
5. Implement user preference learning

## Documentation

When updating documentation:

- Keep language clear and simple
- Include code examples
- Add screenshots for UI changes
- Update the table of contents
- Check for broken links

## Pull Request Process

1. **Update Documentation**: Ensure all docs are updated
2. **Run Tests**: All tests must pass
3. **Write Clear Commit Messages**: Describe what and why
4. **One Feature Per PR**: Keep PRs focused
5. **Respond to Feedback**: Address review comments promptly

### Commit Message Format

```
<type>: <short summary>

<detailed description>

<breaking changes if any>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat: Add support for Kyoto region clinics

- Added Kyoto areas to location data
- Updated scraper to handle Kyoto-specific formatting
- Added tests for Kyoto clinics
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## Getting Help

- Read the README.md and USAGE.md
- Check existing issues and PRs
- Ask questions in new issues
- Join discussions in PRs

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project website (future)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with your questions or reach out to the maintainers.

Thank you for contributing to PROJECT BEAUTY! 🌸
