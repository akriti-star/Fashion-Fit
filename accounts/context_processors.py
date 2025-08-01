def user_preferences(request):
    """Add user login preferences to context"""
    context = {}
    
    if request.user.is_authenticated:
        # Get user's login preference from session
        login_as = request.session.get('login_as', request.user.user_type)
        context['current_login_as'] = login_as
        
        # Add permission checks
        context['can_access_buyer_features'] = request.user.is_buyer()
        context['can_access_seller_features'] = request.user.is_seller()
        context['can_sell_products'] = request.user.can_sell()
        
        # Add user type information
        context['user_is_buyer'] = request.user.is_buyer()
        context['user_is_seller'] = request.user.is_seller()
        context['user_is_verified_seller'] = request.user.is_verified_seller
        
    return context
