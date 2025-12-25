#!/usr/bin/env python3
"""
Run the Streamlit Analytics Dashboard
"""
import os
import subprocess
import sys

def run_dashboard():
    """Run the Streamlit dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')

    # Set environment variables for Streamlit
    env = os.environ.copy()
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_SERVER_PORT'] = '8501'

    print("🚀 Starting DAMP Analytics Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("💡 Press Ctrl+C to stop the dashboard")

    try:
        # Run streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', dashboard_path,
            '--server.port', '8501',
            '--server.headless', 'true'
        ], env=env, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_dashboard()
