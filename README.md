# record_company_api
Record label company API

## Installation

Install record-company-api with docker-compose

```bash
  git clone https://gitlab.com/konnektable-devops/management/hiring-assessments/dionysis-polyzos-backend-ha.git
  cd dionysis-polyzos-backend-ha
  docker-compose build
  docker-compose up
```

## API Endpoints

| Endpoints     | 
|---------------| 
| /artist/      |
| /album/       |
| /track/       |
| /search/      |
| /subscription/ |
| /customer/    |
| /auth/users/  |

/customer/ is admin only

/users/ see [djoser](https://djoser.readthedocs.io/en/latest/getting_started.html) documentation

## Extra

Requires a daily celery job to clean expired subscriptions from users