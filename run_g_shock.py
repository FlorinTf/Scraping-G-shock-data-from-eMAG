from Emag_G_Shock import Emag_bot

with Emag_bot() as emag:

    emag.GDPR()
    emag.Searchbox('g-shock')
    emag.database()