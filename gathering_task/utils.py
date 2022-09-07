# -*- coding: utf-8 -*-
import importlib
from typing import Tuple, List, Dict, Iterable

from gathering_task.task_runner import Task


def build_tasks_with_name_args(task_names: Iterable[str], moudle_name: str, package: str = None) -> List[Task]:
    """通过含有任务类名和参数的字符串构建任务对象"""
    if not task_names:
        return []

    tasks = []
    for task_name in task_names:
        mod = importlib.import_module(moudle_name, package)
        if ':' in task_name:
            task_name, args_str = task_name.split(':', 1)
            args, kwargs = get_args_kwargs_from_string(args_str)
            task = getattr(mod, task_name)(*args, **kwargs)
        else:
            task = getattr(mod, task_name)()
        tasks.append(task)

    return tasks


def get_args_kwargs_from_string(args_str: str) -> Tuple[List[str], Dict[str, str]]:
    """从字符串解析参数，多个参数可用逗号分隔，支持用 k=v 方式传递关键字参数"""
    result_args = []
    result_kwargs = {}

    arg_str_list = args_str.split(',')
    for arg_str in arg_str_list:
        if '=' in arg_str:
            k, v = arg_str.split('=', 1)
            result_kwargs[k] = v
        else:
            result_args.append(arg_str)

    return result_args, result_kwargs
