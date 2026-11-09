#!/usr/bin/env python3
"""Static regression checks only; not a Shadowrocket runtime or a phone test."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "archive/guan-20260929.conf"
NEW = ROOT / "guan.conf"
ADDED = [
    "DOMAIN-SUFFIX,oaistatsig.com,ChatGPT",
    "DOMAIN,challenges.cloudflare.com,ChatGPT",
    "DOMAIN,cdn.workos.com,ChatGPT",
    "DOMAIN,forwarder.workos.com,ChatGPT",
    "DOMAIN,setup.workos.com,ChatGPT",
    "DOMAIN,frontend-apps-multi-region.workos.com,ChatGPT",
    "DOMAIN,images.workoscdn.com,ChatGPT",
    "DOMAIN,workos.imgix.net,ChatGPT",
]

def sections(path):
    result = {}
    section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            assert section not in result, "Duplicate section"
            result[section] = []
        else:
            assert section, "Setting outside a section"
            result[section].append(line)
    return result

def match(rules, domain, cn=False):
    for line in rules:
        parts = line.split(",")
        kind = parts[0]
        if kind == "DOMAIN" and domain == parts[1]:
            return parts[2]
        if kind == "DOMAIN-SUFFIX" and (domain == parts[1] or domain.endswith("." + parts[1])):
            return parts[2]
        if kind == "DOMAIN-KEYWORD" and parts[1] in domain:
            return parts[2]
        if kind == "GEOIP" and parts[1] == "CN" and cn:
            return parts[2]
        if kind == "FINAL":
            return parts[1]
    return None

def main():
    old, new = sections(OLD), sections(NEW)
    assert set(old) == set(new) == {"General", "Proxy Group", "Rule", "URL Rewrite"}
    for section in ("General", "Proxy Group", "URL Rewrite"):
        assert old[section] == new[section], section + " unexpectedly changed"
    assert [x for x in new["Rule"] if x not in ADDED] == old["Rule"], "Existing rule order changed"
    assert len(new["Rule"]) - len(old["Rule"]) == len(ADDED)
    assert len(new["Rule"]) == len(set(new["Rule"])), "Duplicate rules"
    for rule in ADDED:
        assert new["Rule"].count(rule) == 1

    groups = {}
    for line in new["Proxy Group"]:
        name, definition = line.split("=", 1)
        name = name.strip()
        assert name not in groups
        groups[name] = [x.strip() for x in definition.split(",")]
    for group in ("ChatGPT", "xai", "官"):
        assert groups[group][:5] == ["fallback", "奶昔-香港", "奶昔-日本", "奶昔-新加坡", "奶昔-美国"]
        assert "狗狗" not in groups[group]
    for parts in groups.values():
        assert parts[0] in ("select", "fallback")
        for member in parts[1:]:
            if "=" not in member:
                assert member in groups or member in ("DIRECT", "REJECT")
            elif member.startswith("policy-regex-filter="):
                re.compile(member.split("=", 1)[1])
    for line in new["Rule"]:
        parts = line.split(",")
        target = parts[1] if parts[0] == "FINAL" else parts[2]
        assert target in groups or target in ("DIRECT", "REJECT"), "Missing rule target"

    changed_hosts = {line.split(",")[1] for line in ADDED}
    route_cases = {
        "chatgpt.com": "ChatGPT", "ws.chatgpt.com": "ChatGPT",
        "auth.openai.com": "ChatGPT", "files.oaiusercontent.com": "ChatGPT",
        "chatgpt.livekit.cloud": "ChatGPT", "cdn.oaistatic.com": "ChatGPT",
        "api.x.ai": "xai", "grok.com": "xai", "x.com": "xai",
        "cursor.com": "xai", "api.workos.com": "xai",
        "google.com": "官", "drive.google.com": "官", "youtube.com": "官",
        "qq.com": "DIRECT", "weixin.qq.com": "DIRECT", "10086.cn": "DIRECT",
    }
    route_cases.update({host: "ChatGPT" for host in changed_hosts})
    route_cases["feature.oaistatsig.com"] = "ChatGPT"
    for host, expected in route_cases.items():
        assert match(new["Rule"], host) == expected, host
        assert match(new["Rule"], host, cn=True) == expected, host + " changed by GEOIP"
    probes = set()
    for line in old["Rule"]:
        parts = line.split(",")
        if parts[0] in ("DOMAIN", "DOMAIN-SUFFIX"):
            probes.update([parts[1], "www." + parts[1]])
    for host in probes - changed_hosts:
        for cn in (False, True):
            assert match(old["Rule"], host, cn) == match(new["Rule"], host, cn), host
    text = NEW.read_text()
    assert "[Proxy]" not in text and "[MITM]" not in text and "[Script]" not in text
    assert not re.search(r"(?i)(?:password|authorization|access_token)\s*[:=]", text)
    print(f"PASS: {len(ADDED)} allowlisted additions; {len(route_cases) * 2} routing checks; "
          f"{len(probes - changed_hosts) * 2} unchanged-domain checks; groups/General/rewrite preserved")

if __name__ == "__main__":
    main()
