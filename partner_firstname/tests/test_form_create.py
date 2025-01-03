from odoo.addons.base.tests.test_form_create import TestFormCreate

def test_create_res_partner(self):
    # YTI: Clean that brol
    if hasattr(self.env['res.partner'], 'property_account_payable_id'):
        # Required for `property_account_payable_id`, `property_account_receivable_id` to be visible in the view
        # By default, it's the `group` `group_account_readonly` which is required to see it, in the `account` module
        # But once `account_accountant` gets installed, it becomes `account.group_account_manager`
        # https://github.com/odoo/enterprise/blob/bfa643278028da0bfabded2f87ccb7e323d697c1/account_accountant/views/product_views.xml#L9
        self.env.user.groups_id += self.env.ref('account.group_account_readonly')
        self.env.user.groups_id += self.env.ref('account.group_account_manager')
    partner_form = Form(self.env['res.partner'])
    partner_form.firstname = 'a'
    partner_form.lastname = 'partner'
    # YTI: Clean that brol
    if hasattr(self.env['res.partner'], 'property_account_payable_id'):
        property_account_payable_id = self.env['account.account'].create({
            'name': 'Test Account',
            'account_type': 'liability_payable',
            'code': 'TestAccountPayable',
            'reconcile': True
        })
        property_account_receivable_id = self.env['account.account'].create({
            'name': 'Test Account',
            'account_type': 'asset_receivable',
            'code': 'TestAccountReceivable',
            'reconcile': True
        })
        partner_form.property_account_payable_id = property_account_payable_id
        partner_form.property_account_receivable_id = property_account_receivable_id
    partner_form.save()

TestFormCreate.test_create_res_partner = test_create_res_partner
