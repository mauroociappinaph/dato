#!/usr/bin/env python3
"""
Visual Learning Engine - Domain Classifier
Logic for classifying visual content domains and generating semantic search terms.
"""

from typing import List, Dict

class DomainClassifier:
    """Classifies content and optimizes search strategy by domain"""

    def __init__(self):
        self.domains = {
            'development': ['coding', 'programming', 'implementation', 'build'],
            'design': ['ui', 'ux', 'interface', 'visual', 'creative'],
            'business': ['workflow', 'process', 'management', 'strategy'],
            'data': ['analysis', 'visualization', 'processing', 'insights'],
            'deployment': ['hosting', 'cloud', 'infrastructure', 'scaling']
        }

    def classify(self, title: str, description: str) -> str:
        """Identify content domain from text metadata"""
        text = f"{title} {description}".lower()
        for domain, keywords in self.domains.items():
            if any(k in text for k in keywords):
                return domain
        return 'general'

    def generate_search_terms(self, task: str, domain: str = None) -> List[str]:
        """Generate optimized search terms for acquisition"""
        terms = set(task.lower().split())
        if domain and domain in self.domains:
            terms.update(self.domains[domain])
        terms.update(['tutorial', 'how to', 'guide', 'step by step'])
        return list(terms)

    def is_tutorial(self, title: str, description: str) -> bool:
        """Determine if content is instructional"""
        indicators = ['tutorial', 'how to', 'guide', 'step by step', 'learn', 'beginner']
        text = f"{title} {description}".lower()
        return any(i in text for i in indicators)
