# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from api_business.FusionAuthService import FusionAuthService
from api_business.ATGAccountService import ATGAccountService
from lenspackage.LensPackageConstant import CA_REGION, US_REGION
from lenspackage.LensPackageGeneratorService import LensPackageGeneratorService
from settings import yaml_cfg

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # fusion_auth_service = FusionAuthService(region=CA_REGION)
    #
    # token_value = fusion_auth_service.login(
    #     login_id="apitest1@ca.com",
    #     password="Zn@12345",
    #     ip_address="192.168.1.42"
    # )
    #
    # # Call the get_current_user API
    # atg_account_service = ATGAccountService(
    #     session=fusion_auth_service.session,
    #     token_value=token_value,
    #     region=CA_REGION)
    # current_user = atg_account_service.get_current_user()
    # # print("Current User:", current_user)
    #
    #
    # lens_package_service = LensPackageGeneratorService(session=fusion_auth_service.session, token_value=token_value, region=CA_REGION)
    # lens_package_service.generateJsonFile()

    us_fusion_auth_service = FusionAuthService(region=US_REGION)

    us_token_value = us_fusion_auth_service.login(
        login_id="apitest1@us.com",
        password="Zn@12345",
        ip_address="192.168.1.42"
    )

    # Call the get_current_user API
    us_atg_account_service = ATGAccountService(
        session=us_fusion_auth_service.session,
        token_value=us_token_value,
        region=US_REGION)
    current_user = us_atg_account_service.get_current_user()
    # print("Current User:", current_user)

    us_lens_package_service = LensPackageGeneratorService(
        session=us_fusion_auth_service.session,
        token_value=us_token_value,
        region=US_REGION)
    us_lens_package_service.generateJsonFile()
