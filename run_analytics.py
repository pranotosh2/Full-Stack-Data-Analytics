#!/usr/bin/env python3
"""
Quick script to run the analytics dashboard
"""
import os
import sys
import subprocess

def main():
    """Run the Streamlit analytics dashboard"""
    # Check if we're in the right directory
    if not os.path.exists('backend/analytics/dashboard.py'):
        print("❌ Error: Please run this script from the project root directory")
        print("Example: python run_analytics.py")
        sys.exit(1)

    # Check if required packages are installed
    try:
        import streamlit
        import plotly
    except ImportError:
        print("📦 Installing required packages...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'streamlit', 'plotly'
        ], check=True)
        print("✅ Packages installed successfully!")

    print("🚀 Starting DAMP Analytics Dashboard...")
    print("=" * 50)
    print("📊 Dashboard Features:")
    print("  • Real-time platform metrics")
    print("  • Interactive visualizations")
    print("  • User analytics and trends")
    print("  • Course performance insights")
    print("  • Student performance analysis")
    print("  • Mentor effectiveness metrics")
    print("=" * 50)

    # Change to analytics directory and run dashboard
    analytics_dir = os.path.join('backend', 'analytics')
    dashboard_file = os.path.join(analytics_dir, 'dashboard.py')

    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', dashboard_file,
            '--server.port', '8501',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ], cwd=analytics_dir, check=True)
    except KeyboardInterrupt:
        print("\n👋 Analytics dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        print("💡 Make sure:")
        print("   - PostgreSQL is running")
        print("   - Database is properly configured")
        print("   - All dependencies are installed")
        sys.exit(1)

if __name__ == "__main__":
    main()
