from odoo.tests import Form
from odoo.addons.base.tests.test_res_users import TestUsers2

def test_change_user_login(self):
    """ Check that partner email is updated when changing user's login """

    User = self.env['res.users']
    with Form(User, view='base.view_users_form') as UserForm:
        UserForm.firstname = "Test"
        UserForm.lastname = "User"
        UserForm.login = "test-user1"
        self.assertFalse(UserForm.email)

        UserForm.login = "test-user1@mycompany.example.org"
        self.assertEqual(
            UserForm.email, "test-user1@mycompany.example.org",
            "Setting a valid email as login should update the partner's email"
        )

def test_reified_groups(self):
        """ The groups handler doesn't use the "real" view with pseudo-fields
        during installation, so it always works (because it uses the normal
        groups_id field).
        """
        # use the specific views which has the pseudo-fields
        f = Form(self.env['res.users'], view='base.view_users_form')
        f.firstname = "bob"
        f.login = "bob"
        user = f.save()

        self.assertIn(self.env.ref('base.group_user'), user.groups_id)

        # all template user groups are copied
        default_user = self.env.ref('base.default_user')
        self.assertEqual(default_user.groups_id, user.groups_id)

def test_reified_groups_on_change(self):
        """Test that a change on a reified fields trigger the onchange of groups_id."""
        group_public = self.env.ref('base.group_public')
        group_portal = self.env.ref('base.group_portal')
        group_user = self.env.ref('base.group_user')

        # Build the reified group field name
        user_groups = group_public | group_portal | group_user
        user_groups_ids = [str(group_id) for group_id in sorted(user_groups.ids)]
        group_field_name = f"sel_groups_{'_'.join(user_groups_ids)}"

        # <group col="4" invisible="sel_groups_1_9_10 != 1" groups="base.group_no_one" class="o_label_nowrap">
        with self.debug_mode():
            user_form = Form(self.env['res.users'], view='base.view_users_form')
        user_form.firstname = "Test"
        user_form.login = "Test"
        self.assertFalse(user_form.share)

        user_form[group_field_name] = group_portal.id
        self.assertTrue(user_form.share, 'The groups_id onchange should have been triggered')

        user_form[group_field_name] = group_user.id
        self.assertFalse(user_form.share, 'The groups_id onchange should have been triggered')

        user_form[group_field_name] = group_public.id
        self.assertTrue(user_form.share, 'The groups_id onchange should have been triggered')

TestUsers2.test_change_user_login = test_change_user_login
TestUsers2.test_reified_groups = test_reified_groups
TestUsers2.test_reified_groups_on_change = test_reified_groups_on_change
