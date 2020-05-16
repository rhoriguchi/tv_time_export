# tv_time_export

This project runs with python3.

It logs in to [Tv Time](https://www.tvtime.com) with the specified user and extracts the watched status of all tv shows and saves them as easy to read html file.

## Install

python setup.py install

## Run

If no `configPath` is given, it searches in current directory for `config.yaml`.

```
tv_time_export configPath
```

## config.yaml

If no `sava_path` is given, it creates in current dir `exports` folder.

```yaml
username: ****
password: ****
sava_path: /tmp/exports
```
