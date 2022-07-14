# etcd-watcher

[![tests](https://github.com/pycasbin/etcd-watcher/actions/workflows/release.yml/badge.svg)](https://github.com/pycasbin/etcd-watcher/actions/workflows/release.yml)[![Coverage Status](https://coveralls.io/repos/github/pycasbin/etcd-watcher/badge.svg)](https://coveralls.io/github/pycasbin/etcd-watcher)[![Version](https://img.shields.io/pypi/v/casbin-etcd-watcher.svg)](https://pypi.org/project/casbin-etcd-watcher/)[![Download](https://img.shields.io/pypi/dm/casbin-etcd-watcher.svg)](https://pypi.org/project/casbin-etcd-watcher/)[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/casbin/lobby)

Etcd Watcher is the [Etcd](https://github.com/coreos/etcd) watcher for [pycasbin](https://github.com/casbin/pycasbin). With this library, Casbin can synchronize the policy with the database in multiple enforcer instances.

## Installation

    pip install casbin-etcd-watcher

## Simple Example

```python
import casbin
from etcd_watcher import new_watcher

def update_callback_func(event):
    ...

watcher = new_watcher(endpoints=["localhost", 2379], keyname="/casbin")
watcher.set_update_callback(update_callback_func)

e = casbin.Enforcer(
	get_examples("rbac_model.conf"), get_examples("rbac_policy.csv")
)

e.set_watcher(watcher)
# update_callback_func will be called
e.save_policy()
```

## Getting Help

- [Casbin](https://github.com/casbin/pycasbin)

## License

This project is under Apache 2.0 License. See the [LICENSE](LICENSE) file for the full license text.
