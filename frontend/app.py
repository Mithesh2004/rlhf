"""
Main application entry point for the Doctor Session Portal
"""
from src.utils.ui_components import setup_page_config, apply_custom_css
from src.utils.session_state import initialize_session_state, get_session_state
from src.pages.login import login_page
from src.pages.conversation import conversation_page
from src.pages.conversation_detail import conversation_detail_page

def main():
    """Main application entry point"""
    # Initialize the application
    setup_page_config()
    apply_custom_css()
    initialize_session_state()
    
    # Route to the appropriate page
    current_page = get_session_state('current_page')
    if current_page == 'login':
        login_page()
    elif current_page == 'conversation':
        conversation_page()
    elif current_page == 'conversation_detail':
        conversation_detail_page()

if __name__ == "__main__":
    main()