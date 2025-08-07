"""
Marketing Code Management for Yourl.Cloud Nonprofit
Handles generation, tracking, and auditing of marketing/project codes
"""

import os
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

class MarketingCodeManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.code_file = "codes/marketing_codes.json"
        self._ensure_code_directory()

    def _ensure_code_directory(self):
        """Ensure the codes directory exists"""
        os.makedirs("codes", exist_ok=True)

    def _generate_code(self, prefix: str, context: Dict) -> str:
        """
        Generate a marketing code based on context
        Format: PREFIX-YYYYMMDD-XXXX where XXXX is a hash of context
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        context_str = json.dumps(context, sort_keys=True)
        hash_part = hashlib.sha256(context_str.encode()).hexdigest()[:4].upper()
        return f"{prefix}-{timestamp}-{hash_part}"

    def get_current_codes(self) -> Tuple[str, str]:
        """
        Get current and next public marketing codes
        Returns: (current_public_code, next_public_code)
        """
        try:
            with open(self.code_file, 'r') as f:
                codes = json.load(f)
                return codes.get('current_public_code', ''), codes.get('next_public_code', '')
        except FileNotFoundError:
            return '', ''

    def create_deployment_code(self, context: Dict) -> str:
        """
        Create a new deployment marketing code
        Context should include:
        - commit_sha
        - build_id
        - environment (e.g., 'production', 'staging')
        - features (list of features being deployed)
        - donor_funded_features (list of donor-funded features)
        """
        code = self._generate_code('DEPLOY', context)
        self._save_code_info(code, 'deployment', context)
        return code

    def create_feature_code(self, context: Dict) -> str:
        """
        Create a new feature development marketing code
        Context should include:
        - branch_name
        - feature_description
        - donor_attribution (optional)
        - partner_attribution (optional)
        """
        code = self._generate_code('FEAT', context)
        self._save_code_info(code, 'feature', context)
        return code

    def create_build_code(self, context: Dict) -> str:
        """
        Create a new build marketing code
        Context should include:
        - commit_sha
        - build_id
        - build_trigger
        - features_included
        """
        code = self._generate_code('BUILD', context)
        self._save_code_info(code, 'build', context)
        return code

    def _save_code_info(self, code: str, code_type: str, context: Dict):
        """Save code information for auditing"""
        try:
            with open(self.code_file, 'r') as f:
                codes = json.load(f)
        except FileNotFoundError:
            codes = {'codes': [], 'current_public_code': '', 'next_public_code': ''}

        # Add new code info
        code_info = {
            'code': code,
            'type': code_type,
            'context': context,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'project_id': self.project_id
        }
        codes['codes'].append(code_info)

        # Update public codes if this is a deployment
        if code_type == 'deployment' and context.get('environment') == 'production':
            codes['current_public_code'] = codes.get('next_public_code', '')
            codes['next_public_code'] = code

        # Save updated codes
        with open(self.code_file, 'w') as f:
            json.dump(codes, f, indent=2)

    def get_code_info(self, code: str) -> Optional[Dict]:
        """Get information about a specific marketing code"""
        try:
            with open(self.code_file, 'r') as f:
                codes = json.load(f)
                for code_info in codes['codes']:
                    if code_info['code'] == code:
                        return code_info
        except FileNotFoundError:
            pass
        return None

    def get_codes_by_type(self, code_type: str) -> list:
        """Get all codes of a specific type"""
        try:
            with open(self.code_file, 'r') as f:
                codes = json.load(f)
                return [c for c in codes['codes'] if c['type'] == code_type]
        except FileNotFoundError:
            return []

    def generate_audit_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        """
        Generate an audit report of marketing codes
        Dates should be in ISO format (YYYY-MM-DD)
        """
        try:
            with open(self.code_file, 'r') as f:
                codes = json.load(f)
        except FileNotFoundError:
            return {'error': 'No code history found'}

        report = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'project_id': self.project_id,
            'date_range': {'start': start_date, 'end': end_date},
            'summary': {
                'total_codes': len(codes['codes']),
                'deployments': len([c for c in codes['codes'] if c['type'] == 'deployment']),
                'features': len([c for c in codes['codes'] if c['type'] == 'feature']),
                'builds': len([c for c in codes['codes'] if c['type'] == 'build'])
            },
            'current_public_code': codes.get('current_public_code', ''),
            'next_public_code': codes.get('next_public_code', ''),
            'codes': []
        }

        for code_info in codes['codes']:
            created_at = code_info['created_at']
            if start_date and created_at < start_date:
                continue
            if end_date and created_at > end_date:
                continue
            report['codes'].append(code_info)

        return report

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Yourl.Cloud Marketing Code Management")
    parser.add_argument("--project", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=['create-deployment', 'create-feature', 'create-build', 'get-current', 'audit'],
                      required=True, help="Action to perform")
    parser.add_argument("--context", help="JSON string with context information")
    parser.add_argument("--start-date", help="Start date for audit (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date for audit (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    manager = MarketingCodeManager(args.project)
    
    if args.action == 'get-current':
        current, next_code = manager.get_current_codes()
        print(f"Current public code: {current}")
        print(f"Next public code: {next_code}")
    
    elif args.action == 'audit':
        report = manager.generate_audit_report(args.start_date, args.end_date)
        print(json.dumps(report, indent=2))
    
    else:
        if not args.context:
            print("Error: --context required for create actions")
            exit(1)
        
        context = json.loads(args.context)
        
        if args.action == 'create-deployment':
            code = manager.create_deployment_code(context)
        elif args.action == 'create-feature':
            code = manager.create_feature_code(context)
        else:  # create-build
            code = manager.create_build_code(context)
        
        print(f"Generated code: {code}")
