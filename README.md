# tv_time_export

This project runs with python3.

It logs in to [TV Time](https://www.tvtime.com) with the specified user and extracts the watched status of all tv shows and saves them as json.

## Install

python setup.py install

## Run

If no `configPath` is given, it searches in current directory for `config.yaml`.

```bash
tv_time_export [configPath]
```

## config.yaml

If no `sava_path` is given, it exports to current dir.

```yaml
username: ****
password: ****
sava_path: /tmp/exports
```
