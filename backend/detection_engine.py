"""
Optimized SQL Injection Detection Engine
Fast + Robust + Smart Detection
"""

import re
from ml_model import ml_model


class DetectionEngine:

    def __init__(self):

        # 🔹 Original patterns (FIXED)
        self.dangerous_patterns = [
            (r"'\s*--", "Comment-based injection", "High"),
            (r"#.*$", "Comment-based injection", "High"),
            (r"/\*.*\*/", "Comment-based injection", "High"),

            (r"UNION\s+SELECT", "UNION-based injection", "High"),
            (r"UNION\s+ALL\s+SELECT", "UNION-based injection", "High"),

            (r"DROP\s+TABLE", "DROP TABLE attack", "High"),
            (r"DELETE\s+FROM.*WHERE\s+1\s*=\s*1", "Mass DELETE attack", "High"),

            (r"OR\s+1\s*=\s*1", "Tautology attack", "Medium"),
            (r"OR\s+'[^']*'\s*=\s*'[^']*'", "Tautology attack", "Medium"),
            (r'OR\s+"[^"]*"\s*=\s*"[^"]*"', "Tautology attack", "Medium"),
            (r"OR\s+true", "Tautology attack", "Medium"),

            (r";\s*(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE)", "Stacked queries", "High"),

            (r"WAITFOR\s+DELAY", "Time-based injection", "Medium"),
            (r"BENCHMARK\s*\(", "Time-based injection", "Medium"),
            (r"SLEEP\s*\(", "Time-based injection", "Medium"),

            (r"information_schema", "Schema enumeration", "High"),

            (r"LOAD_FILE\s*\(", "File read attempt", "High"),
            (r"INTO\s+OUTFILE", "File write attempt", "High"),

            (r"xp_cmdshell", "Command execution", "High"),

            (r"GRANT\s+ALL", "Privilege escalation", "High"),

            (r"CONVERT\s*\(", "Error-based injection", "Medium"),

            (r"HAVING\s+1\s*=\s*1", "HAVING injection", "Medium"),

            (r"SELECT.*password\s+FROM", "Credential access", "High"),
        ]

        # 🔥 Precompile regex
        self.compiled_patterns = [
            (re.compile(p, re.IGNORECASE), t, s)
            for p, t, s in self.dangerous_patterns
        ]

    # 🔹 Normalize query
    def normalize_query(self, query):
        query = query.lower()
        query = re.sub(r"/\*.*?\*/", " ", query)
        query = re.sub(r"\s+", " ", query)
        return query.strip()

    # 🔹 Fast keyword filter
    def quick_filter(self, query):
        keywords = ["select", "union", "drop", "insert", "delete", "update", "--", "#"]
        return any(k in query for k in keywords)

    # 🔹 Rule-based detection
    def check_rule_based(self, query):
        for pattern, attack_type, severity in self.compiled_patterns:
            try:
                if pattern.search(query):
                    return {
                        'is_attack': True,
                        'attack_type': attack_type,
                        'severity': severity,
                        'method': 'rule-based',
                        'confidence': 1.0
                    }
            except Exception:
                continue
        return None

    # 🔹 Heuristic scoring
    def heuristic_score(self, query):
        score = 0

        if "or 1=1" in query:
            score += 2
        if "union select" in query:
            score += 3
        if "--" in query or "#" in query:
            score += 1
        if ";" in query:
            score += 1

        return score

    # 🔹 ML detection
    def check_ml_based(self, query):
        prediction = ml_model.predict(query)

        if prediction.get('error'):
            return {
                'is_attack': False,
                'severity': 'Low',
                'method': 'ml-failed',
                'confidence': 0.0
            }

        is_attack = prediction['prediction'] == 'malicious'
        confidence = prediction['confidence']

        return {
            'is_attack': is_attack,
            'severity': 'High' if confidence > 0.8 else 'Medium',
            'method': 'machine-learning',
            'confidence': confidence
        }

    # 🔹 Main function
    def analyze_query(self, query):

        if not query.strip():
            return {
                'is_attack': False,
                'severity': 'Low',
                'method': 'empty',
                'confidence': 1.0,
                'blocked': False,
                'recommendation': 'Empty query'
            }

        query = self.normalize_query(query)

        # ⚡ Quick filter
        if not self.quick_filter(query):
            return {
                'is_attack': False,
                'severity': 'Low',
                'method': 'quick-filter',
                'confidence': 1.0,
                'blocked': False,
                'recommendation': 'Query appears safe'
            }

        # 🔥 Rule-based
        rule = self.check_rule_based(query)
        if rule:
            return {
                **rule,
                'blocked': True,
                'recommendation': 'Malicious pattern detected'
            }

        # 🧠 Heuristic
        score = self.heuristic_score(query)
        if score >= 3:
            return {
                'is_attack': True,
                'attack_type': 'Heuristic detection',
                'severity': 'High',
                'method': 'heuristic',
                'confidence': 0.9,
                'blocked': True,
                'recommendation': 'Suspicious query detected'
            }

        # 🤖 ML fallback
        ml = self.check_ml_based(query)

        return {
            **ml,
            'blocked': ml['is_attack'],
            'recommendation': 'Query appears safe' if not ml['is_attack'] else 'Potential threat detected'
        }


# Initialize
detection_engine = DetectionEngine()