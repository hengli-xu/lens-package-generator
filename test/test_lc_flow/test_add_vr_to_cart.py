from lenspackage.LensPackageConstant import CA_REGION
from api_business.FusionAuthService import FusionAuthService
from api_business.ATGAccountService import ATGAccountService

class TestAddVrToCart:
    def test_add_non_rx_vr_to_cart(self):
        """
        Test to add a VR product to the cart.
        """
        fusion_auth_service = FusionAuthService(region=CA_REGION)

        token_value = fusion_auth_service.login(
            login_id="apitest1@ca.com",
            password="Zn@12345",
            ip_address="192.168.1.42"
        )

        print("Token Value:", token_value)

        # Print session cookies
        print("Session Cookies after login:", fusion_auth_service.session.cookies.get_dict())

        # Call the get_current_user API
        atg_service = ATGAccountService(session=None, token_value=token_value, region=CA_REGION)
        user_data = atg_service.get_current_user()
        print("User Data:", user_data)