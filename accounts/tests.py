from django.contrib.auth import get_user_model
from django.contrib.auth.views import login
from django.test import TestCase

from .factories import (InvitedPendingFactory, ModeratorFactory,
                        RequestedPendingFactory, UserFactory)
from .models import CustomUser

User = get_user_model()


# Models.py

class UserModelTest(TestCase):

    def setUp(self):
        self.moderator = ModeratorFactory()
        self.standard = UserFactory()
        self.invited_pending = InvitedPendingFactory()
        self.requested_pending = RequestedPendingFactory()

    def test_moderator_can_invite_new_user(self):
        user = self.moderator.invite_new_user(email='standard@test.test',
                                              first_name='standard',
                                              last_name='user')

        self.assertEqual(user.email,'standard@test.test')
        self.assertEqual(user.first_name, 'standard')
        self.assertEqual(user.last_name, 'user')
        self.assertEqual(user.registration_method, CustomUser.INVITED)
        self.assertEqual(user.moderator, self.moderator)
        self.assertEqual(user.moderator_decision, CustomUser.PRE_APPROVED)
        self.assertIsNotNone(user.decision_datetime)
        self.assertIsNotNone(user.auth_token)

    def test_standard_user_cannot_invite_new_user(self):
        user = self.standard.invite_new_user(email='standard@test.test',
                                             first_name='standard',
                                             last_name='user')

        self.assertIsNone(user)

    def test_moderator_can_reinvite_user(self):

        decision_datetime = self.invited_pending.decision_datetime
        auth_token = self.invited_pending.auth_token

        self.moderator.reinvite_user(user=self.invited_pending,
                                     email='reset_email@test.test')

        self.assertEqual(self.invited_pending.email, 'reset_email@test.test')
        self.assertNotEqual(self.invited_pending.decision_datetime, decision_datetime)
        self.assertNotEqual(self.invited_pending.auth_token, auth_token)

    def test_standard_user_cannot_reinvite_user(self):

        decision_datetime = self.invited_pending.decision_datetime
        auth_token = self.invited_pending.auth_token

        self.standard.reinvite_user(user=self.invited_pending,
                                    email='reset_email@test.test')

        self.assertNotEqual(self.invited_pending.email, 'reset_email@test.test')
        self.assertEqual(self.invited_pending.decision_datetime, decision_datetime)
        self.assertEqual(self.invited_pending.auth_token, auth_token)

    def test_moderator_can_approve_user_application(self):
        self.moderator.approve_user_application(self.requested_pending)

        self.assertEqual(self.requested_pending.moderator, self.moderator)
        self.assertEqual(self.requested_pending.moderator_decision, CustomUser.APPROVED)
        self.assertIsNotNone(self.requested_pending.decision_datetime)
        self.assertIsNotNone(self.requested_pending.auth_token)

    def test_standard_user_cannot_approve_user_application(self):
        self.standard.approve_user_application(self.requested_pending)

        self.assertIsNone(self.requested_pending.moderator)
        self.assertFalse(self.requested_pending.moderator_decision)
        self.assertIsNone(self.requested_pending.decision_datetime)
        self.assertFalse(self.requested_pending.auth_token)

    def test_moderator_can_reject_user_application(self):
        self.moderator.reject_user_application(self.requested_pending)

        self.assertEqual(self.requested_pending.moderator, self.moderator)
        self.assertEqual(self.requested_pending.moderator_decision, CustomUser.REJECTED)
        self.assertIsNotNone(self.requested_pending.decision_datetime)
        self.assertIsNotNone(self.requested_pending.auth_token)

    def test_standard_user_cannot_reject_user_application(self):
        self.standard.reject_user_application(self.requested_pending)

        self.assertIsNone(self.requested_pending.moderator)
        self.assertFalse(self.requested_pending.moderator_decision)
        self.assertIsNone(self.requested_pending.decision_datetime)
        self.assertFalse(self.requested_pending.auth_token)


#~class UserSkillTest(TestCase):

    #~def test_proficiency_percentage_calculates_correctly(self):

#~class UserLinkTest(TestCase):
#~
    #~def test_custom_save_method_sets_icon(self):
    #~def test_get_icon_method_gets_correct_icon(self):

#~class LinkBrandTest(TestCase):
    #~def test_custom_save_method_applies_new_brand_to_existing_userlinks(self):


# Forms.py

#~class FormValidationTest(TestCase):
    #~def test_email_availability_validation_passes_with_new_email(self):
    #~def test_email_availability_validation_fails_with_existing_email(self):
#~
#~class RequestInvitationFormValidationTest(TestCase):
    #~def test_closed_account_promts_custom_validation_message(self):
#~
#~class TestActivateAccountFormValidation(TestCase):
    #~def test_password_validation_fails_when_passwords_are_different(self):
    #~def test_password_validation_passes_when_passwords_are_same(self):
#~
#~class BaseSkillFormsetValidationTest(TestCase):
    #~def test_validation_fails_when_userskill_is_not_unique_to_user(self):
    #~def test_validation_passes_when_userskill_is_unique_to_user(self):
    #~def test_validation_fails_when_userskill_has_skill_but_no_proficiency(self):
    #~def test_validation_fails_when_userskill_has_proficicency_but_no_skill(self):
    #~def test_validation_passes_when_userskill_has_skill_and_proficiency(self):
    #~def test_validation_passes_when_both_skill_and_proficiency_are_empty(self):
#~
#~class BaseLinkFormsetValidationTest(TestCase):
    #~def test_validation_fails_when_link_url_is_not_unique_to_user(self):
    #~def test_validation_passes_when_link_url_is_unique_to_user(self):
    #~def test_validation_fails_when_link_anchor_is_not_unique_to_user(self):
    #~def test_validation_passes_when_link_anchor_is_unique_to_user(self):
    #~def test_validation_fails_when_link_has_anchor_but_no_url(self):
    #~def test_validation_fails_when_link_has_url_but_no_anchor(self):
    #~def test_validation_passes_when_link_has_url_and_anchor(self):
    #~def test_validation_passes_when_both_url_and_anchor_are_empty(self):
#~
#~class AccountSettingsFormValidationTest(TestCase):
    #~def test_current_password_matches_users_password(self):
    #~def test_validation_fails_if_user_tries_to_change_password_without_current_password(self):
    #~def test_validation_fails_if_user_tries_to_change_password_without_confirming_password(self):
    #~def test_password_validation_fails_when_passwords_are_different(self):
    #~def test_password_validation_passes_when_passwords_are_same(self):
#~
#~class CloseAccountFormValidationTest(TestCase):
    #~def test_current_password_matches_users_password(self):


# Utils.py

#~class AccountUtilsTest(TestCase):
    #~def test_create_inactive_user_is_not_active(self):
    #~def test_create_inactive_user_is_standard_user(self):
#~
    #~def test_reactivated_account_token_is_reset(self):


# Urls.py and views.py

#~class RequestInvitationTest(TestCase):
    #~def test_request_invitation_url_resolves_to_request_invitation_view(self):
    #~def test_requested_account_is_saved_as_inactive_user(self):


#~class ActivateAccountTest(TestCase):
    #~def test_activate_account_url_resolves_to_activate_account_view(self):
    #~def test_can_activate_account(self):
    #~def test_notification_emails_are_sent_to_moderators(self):
    #~def test_activated_account_redirects_to_correct_view(self):


#~class ProfileSettingsTest(TestCase):
    #~def test_profile_url_resolves_to_profile_settings_view(self):
    #~def test_profile_is_only_available_to_authenticated_users(self):
    #~def test_profile_form_is_prepopulated_with_users_data(self):
    #~def test_skills_formset_shows_users_skills(self):
    #~def test_links_formset_shows_users_links(self):
    #~def test_can_update_profile(self):
    #~def test_link_is_correctly_matched_to_brand(self):


#~class AccountSettingsTest(TestCase):
    #~def test_account_settings_url_resolves_to_account_settings_view(self):
    #~def test_account_settings_is_only_available_to_autheticated_users(self):
    #~def test_account_settings_form_is_rendered_to_page(self):
    #~def test_email_field_is_prepopulated_with_correct_email(self):
    #~def test_close_account_form_is_rendered_to_page(self):

    #~def test_update_account_url_resolves_to_update_account_view(self):
    #~def test_update_account_is_only_available_to_autheticated_users(self):
    #~def test_update_account_is_only_available_to_POST_data(self):
    #~def test_email_is_updated(self):
    #~def test_password_is_updated_if_submitted(self):
    #~def test_password_is_not_updated_if_it_is_not_submitted(self):

    #~def test_close_account_url_resolves_to_close_account_view(self):
    #~def test_close_account_is_only_available_to_autheticated_users(self):
    #~def test_close_account_is_only_available_to_POST_data(self):
    #~def test_can_close_account(self):
    #~def test_closed_account_is_inactive(self):
    #~def test_closed_account_redirects_to_correct_view(self):


# TODO - need to find out a way to test custom migration (0002)
