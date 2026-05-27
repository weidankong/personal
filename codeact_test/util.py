# -*- coding: utf-8 -*-
"""Shared utility functions for codeact test tools."""


import re


def fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def convert(output: str) -> str:
    """Transform the raw output string before parsing."""
    print(f'============{output}===============')
    if output.find("Exception:") > 0:
        m = re.search(r'(\{.*\})', output, re.DOTALL)
        if m:
            return m.group(1).strip()
    return output
