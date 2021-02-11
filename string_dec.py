#!/usr/bin/env python3
BOTNAME = "Test_Bot"

commands_list = ['help','inventory','balance','shop','buy','sell','gift','exchange',
            'tenant','suggest','bug','join','leave','ping','key','investigate',
            'horror','curse','hatch','gacha','voucher','maintenance','injury']

commands_dict_1 = {
    'inventory': 'Quickly view your Member Database inventory' +
                 ' (does not include character inventories)',
    'balance': 'See your current PD and Shard balance',
    'balance_top': 'View a leaderboard showing members with the highest PD balance',
    'shop': 'View all available shop pages',
    'shop_<"page_number">': 'View individual categories/pages of the shop',
    'buy_<"item">_<"quantity">': 'Purchase items from the shop'
}

commands_dict_2 = {
    'sell_<"item">_<"quantity">':
        "Sell items to the shop and receive 1/4th the item's value in return" +
        "(currency type will depend on the item sold)",
    'gift_<@user>_<"item_name">_<"item_quantity">':
        'Allows you to gift another member anything in your main inventory' +
        ' (except shards). Does not apply to character inventories. ' +
        'PD is considered an "item" for the sake of gifting',
    'exchange_shards_<"quantity">':
        'Exchange shards for PD (1 shard = 50PD, at the time of writing)',
    'tenant':
        "Roll for a random tenant, which includes both a preview image and link"+
        " to the tenant's application",
    'tenant_event':
        'Roll a random tenant from those who are currently active in the event RP',
    'suggest_<"suggestion_here">':
        "If you're not comfortable using the #suggestions channel, you can" +
        " send the mod team an anonymous suggestion which will be reviewed privately"
}

commands_dict_3 = {
    'bug_report_<"report_here">':
        'Send the mod team any bug reports you encounter while using ' +
        BOTNAME + ' so we can work on a fix',
    'join_<"role_name">':
        'Add yourself to select roles (birthdays, investigators, spoilers,' +
        ' raiders, or questers)',
    'leave_<"role_name">': # ADD ROLE NAMES FOR PRONOUNS ETC.
        'Remove yourself from the select roles (birthdays, investigators, ' +
        'spoilers, raiders, or questers)',
    'help':
        'Review all of ' + BOTNAME + "'s available commands and how to use them",
    'NEWping':
        'Allows you to play ping-pong with ' + BOTNAME + ' (and check his response time too).'
}

commands_dict_4 = {
    'key_add_<@user>_<"quantity">':
        "Increases a member's tarnished room key purchase counter. Use this "+
        " command if someone purchases a tarnished room key through dA instead of " + BOTNAME,
    'key_view_<@user>':
        'This will show you the total number of tarnished room keys purchased by this member',
    'key_delete_<@user>_<"quantity">':
        "This will allow you to remove the specified amount of tarnished room "+
        "keys from a member's total amount (useful in the case of an accidental purchase)",
#REEXAMINE THESE AFTER IMPLEMENTATION TO ENSURE NO INPUT CHANGES
    'investigate_<"location_name">_<"optional_item">':
        'Investigate for a member. Locations are required, but items are ' +
        'optional. Remember to account for any curses the character may be ' +
        "afflicted with. Make sure to identify the user you're rolling for " +
        " (but don't use an @) posted either before or after this command.",
    'horror_<"horror_tyype">_<"courage_level">_<"optional_item">_<"optional_curses">':
        'Use this command to fight a horror. "Horror type" and "courage level" ' +
        'are always required. Add in items upon request, and curses if a tenant' +
        "has any. If a tenant has a curse, but is not battling with items, leave " +
        "the quotation marks blank. If a tenant is using an item, but has no " +
        "curse, leave off the last quotation marks. If they have neither one " +
        "of these attributes, leave off quotes for both item and curse.",
    'curse_<"horror_type">':
        'Use this command if a tenant loses a battle with a horror and they' +
        "'re afflicted with a curse which they already have. " + BOTNAME +
        " will re-roll for all available curses that the specified horror " +
        " can afflict until the tenant receives a new curse."
}

commands_dict_5 = {
    'hatch_<"#">_<"fusion_(optional)">_<"color-swapped_(optional)">':
        'Use this command to hatch Mystery Eggs. "Number" is always required '+
        'and specifies the number of eggs to hatch, while "fusion" and "color-'+
        'swapped" are optional if conditions are met. Be aware that ALL eggs '+
        'will hatch as a fusion and/or color-swap if these are included. Traited'+
        ' eggs are best hatched one at a time to avoid risk of error.',
    'gacha':
        "Roll the gacha for a member once they've redeemed a gacha token in " +
        "the shop on dA. Once the item is rolled, place it in the requested " +
        "tenant's inventory (the tenant must be owned by the member). Make " +
        "sure to identify the user you're rolling for (but don't use an !) "+
        "posted either before or after this command.",
    'NEWvoucher_<optional @user>':
        'Used to roll a PD value for a PD coucher redeemed through the shop! ' +
        BOTNAME + "will automatically add this balance to a user's inventory " +
        "if you choose to @ them when running the command"
}

commands_dict_6 = {
    'inventory_add_<@user>_<"existing member database tab name">':
        'This command must be performed for all new members before they can ' +
        "use some of " + BOTNAME + "'s user-personalized command functions",
    'inventory_update_<@user>_<"existing member database tab name">':
        'If someone changes their name on dA and requests to have their Member'+
        ' Database sheet updated with their new account name, run this command'+
        ' to update the tab name for ' + BOTNAME + ', too',
    'inventory_view_<@user>':
        'Allows you to view the current Member Database tab name for this user,'+
        ' stored in ' + BOTNAME,
    'maintenance_<0_or_1>':
        'This will allow you to disable (0) or enable (1) ' + BOTNAME +
        'across the entire server, preventing anyone from using commands',
    'injury_<""random",_or_a_specific_tenant_name">_<"injury_category">':
        'Select either a random or specific tenant and give them a random ' +
        'injury (categories: minor, moderate, severe, critical, or random)'
}


emoji_numbers = [
    "1\u20e3","2\u20e3","3\u20e3","4\u20e3","5\u20e3","6\u20e3"
    #,"7\u20e3","8\u20e3","9\u20e3",u"\U0001F51F"
]

help_footer = 'Click on the # reaction to flip through the pages '
help_footer_done = 'Too slow! Enter c!help again to see another page '

welcome_str = ", AWAKEN MY MASTERS!"
invalid_command = "I don't know how to do that, maybe try c!help?"


maintenance_off_text = "Taking the server down for maintenance..."
maintenance_on_text = "Bringing the server online!"
maintenance_wrong_text = "This requires a 0 to turn off or a 1 to turn on."
maintenance_block_text = "0w0 what's this? I'm down fow maintenance wight noww T.T"
