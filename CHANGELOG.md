# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-10-25

### Added
- Initial skeleton: Docker, docker-compose, FastAPI, StaticFiles
- Health check endpoint `/health`
- Base index.html with Bootstrap 5
- 10 legal document templates (HTML→PDF via WeasyPrint)
  - Для самозанятых: счёт, акт, договор, чек
  - Для физлиц: дарение, расписка, займ, акт, ПДн, заявление в ФНС
- Auto-fill from open data APIs (List-Org, KontragentPro, Checko.ru)
- Local bank directory (BIK → bank name)
- Currency rates from CBR API
- Local storage drafts with clear button
- Privacy policy and disclaimers
- pytest and Playwright e2e tests
- GitHub Actions CI pipeline
