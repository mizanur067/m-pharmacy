# Project conventions

- Backend domain logic belongs in services, not views or serializers.
- API routes are versioned under `/api/v1/`.
- Authorization is enforced by DRF permissions; frontend guards are only UX.
- Files use S3-compatible storage configured through environment variables.
- Keep TypeScript strict and avoid `any`.
- Run backend pytest and frontend lint/build before completing a phase.

