## An async API client for LingXing (领星) ERP

Created to be used in a project, this package is published to github for ease of management and installation across different modules.

## Installation

Install from `PyPi`

```bash
pip install lingxingapi
```

Install from `github`

```bash
pip install git+https://github.com/AresJef/LingXingApi.git
```

## Requirements

- Python 3.10 or higher.

## Example

```python
from lingxingapi import API

# Context Manager
async def test(self, app_id: str, app_secret: str) -> None:
    async with API(app_id, app_secret) as api:
        sellers = await api.basic.Sellers()

# Close Manually
async def test(self, app_id: str, app_secret: str) -> None:
    api = API(app_id, app_secret)
    sellers = await api.basic.Sellers()
    await api.close()
```

### Acknowledgements

LingXingApi is based on several open-source repositories.

- [aiohttp](https://github.com/aio-libs/aiohttp)
- [cytimes](https://github.com/AresJef/cyTimes)
- [numpy](https://github.com/numpy/numpy)
- [orjson](https://github.com/ijl/orjson)
- [pydantic](https://github.com/pydantic/pydantic)
