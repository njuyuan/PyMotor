# Copyright (c) Huawei Technologies Co., Ltd. 2025-2026. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import sys
from pathlib import Path

DEPLOYER_ROOT = Path(__file__).resolve().parents[3] / "examples" / "deployer"
sys.path.insert(0, str(DEPLOYER_ROOT))

import lib.constant as C  # noqa: E402
from lib.generator.kv_pool import gen_kv_pool_env, normalize_kv_cache_pool_config  # noqa: E402


def test_gen_kv_pool_env_fills_eviction_defaults():
    user_config = {
        C.KV_CACHE_POOL_CONFIG: {
            "metadata_server": "P2PHANDSHAKE",
            "protocol": "ascend",
            "global_segment_size": "1GB",
        }
    }
    kv_pool_config = normalize_kv_cache_pool_config(user_config)
    env = gen_kv_pool_env(kv_pool_config)
    env_map = {item[C.NAME]: item[C.VALUE] for item in env}

    assert env_map[C.ENV_KV_POOL_PORT] == str(C.DEFAULT_KV_POOL_PORT)
    assert env_map[C.ENV_KV_POOL_EVICTION_HIGH_WATERMARK_RATIO] == str(
        C.DEFAULT_KV_POOL_EVICTION_HIGH_WATERMARK_RATIO
    )
    assert env_map[C.ENV_KV_POOL_EVICTION_RATIO] == str(C.DEFAULT_KV_POOL_EVICTION_RATIO)


def test_gen_kv_pool_env_keeps_explicit_eviction_values():
    user_config = {
        C.KV_CACHE_POOL_CONFIG: {
            "port": 50099,
            "eviction_high_watermark_ratio": 0.8,
            "eviction_ratio": 0.2,
        }
    }
    kv_pool_config = normalize_kv_cache_pool_config(user_config)
    env = gen_kv_pool_env(kv_pool_config)
    env_map = {item[C.NAME]: item[C.VALUE] for item in env}

    assert env_map[C.ENV_KV_POOL_PORT] == "50099"
    assert env_map[C.ENV_KV_POOL_EVICTION_HIGH_WATERMARK_RATIO] == "0.8"
    assert env_map[C.ENV_KV_POOL_EVICTION_RATIO] == "0.2"
