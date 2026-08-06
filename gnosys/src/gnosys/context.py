# SPDX-License-Identifier: AGPL-3.0-only
# gnosys context module
# Copyright (C) 2026 Leonardo Rossetti

import contextvars
from typing import Any


ctx: contextvars.ContextVar[Any] = contextvars.ContextVar('gnosys', default=None)
