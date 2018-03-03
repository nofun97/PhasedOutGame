from itertools import permutations, combinations, combinations_with_replacement
from collections import defaultdict as dd
import copy


def wild_counter(group):
    '''
    wild_counter takes a group of cards in a list and returns an integer
    showing how many aces there are
    '''
    count = 0

    # iterate through the cards in the group
    for card in group:
        if 'A' in card:
            count += 1
    return count


def same_checker(group, base):
    '''
    same_checker takes a group of cards in the form of a list and also a string
    called base and it returns a boolean showing if the group has the same
    attributes
    '''

    # removing aces in the group
    group = [card for card in group if 'A' not in card]

    for index in range(len(group) - 1):
        # to check the values
        if base == 'Value':

            # if the values are different it returns False
            if group[index][0] != group[index + 1][0]:
                return False

        # to check the suits
        elif base == 'Suit':

            # if the suits are different it returns False
            if group[index][-1] != group[index + 1][-1]:
                return False

        # to check the colors
        elif base == 'Color':

            # if the colors are different it returns False
            colors = {'C': 'Black', 'S': 'Black', 'D': 'Red', 'H': 'Red'}
            if colors[group[index][-1]] != colors[group[index + 1][-1]]:
                return False

    return True


def order_checker(group):
    '''
    order_checker takes a group of cards in the form of a list and it returns
    a boolean showing if the group is in a sequence
    '''

    scores = {
        '2': 0,
        '3': 1,
        '4': 2,
        '5': 3,
        '6': 4,
        '7': 5,
        '8': 6,
        '9': 7,
        '0': 8,
        'J': 9,
        'Q': 10,
        'K': 11
    }
    wilds = 0

    # iterating through the cards
    for card in group:

        # if it find an ace it deviates the base variable
        if 'A' in card:
            wilds += 1

        # when it finds a non-wild, it sets the base value
        if card[0] in scores:
            base = scores[card[0]] - wilds
            break

    for index in range(len(group)):
        x = group[index][0]

        # to avoid aces put in front of Kings and cases where base are not
        # declared because all cards are aces
        if len(group) == wilds or base > 11:
            return False

        # if it finds an ace, it skips
        if 'A' in group[index]:
            pass

        # for the value of the index to be lower is impossible
        # the base has to be the same as the value of the card
        elif scores[x] < index or base != scores[x]:
            return False

        # it adds the base
        base += 1
    return True


def phasedout_group_type(group):
    '''
    function phasedout_group_type takes a list of strings of two characters
    which represent a card name and returns an integer from 1 to 5 that
    represents a type of group of the cards or None if the group of cards
    does not belong to any of the group types
    '''

    # finding the number of cards
    num_of_cards = len(group)

    # finding the number of wilds
    wilds = wild_counter(group)

    # if there are at least 2 natural cards
    if num_of_cards - wilds >= 2:

        # to check if the values are the same and the length is 3 cards
        if same_checker(group, 'Value') and num_of_cards == 3:
            return 1

        # to check if the suits are the same and the length is 7 cards
        elif same_checker(group, 'Suit') and num_of_cards == 7:
            return 2

        # to check if the values are the same and the length is 4 cards
        elif same_checker(group, 'Value') and num_of_cards == 4:
            return 3

        # to check if the colors are the same
        # if it is also in a sequence and anscending order
        # and the length is 4 cards
        elif same_checker(group, 'Color') and order_checker(group) \
        and num_of_cards == 4:
            return 5

        # to check if it is in a sequence and anscending also the length is 8
        elif order_checker(group) and num_of_cards == 8:
            return 4

    return None


def phasedout_phase_type(phase):
    '''
    phasedout_phase_type takes a nested list called phase and returns an
    integer that shows the type of the group of phase and returns None
    when phase does not belong to any group
    '''

    card_type = []
    results = {(1, 1): 1, (2, ): 2, (3, 3): 3, (4, ): 4, (5, 3): 5}

    # iterate through the groups in phase
    for cards in phase:
        # checking the type of groups in phase
        types = phasedout_group_type(cards)

        #putting the types of groups into a list
        card_type.append(types)

    try:
        # calling certain keys to return the phase type
        return results[tuple(card_type)]
    except KeyError:
        # if the groups do not belong in any phase type, it returns none
        return None


def phasedout_score(hand):
    '''
    phasedout_score takes a list of cards named hand and returns an integer
    that represents the score of the hand
    '''

    if hand != []:
        score = 0
        scores = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '0': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 25
        }

        # iterate through the hand
        for card in hand:

            # adding the score
            score += scores[card[0]]
        return score
    return 0


def player_rotation(player):
    '''
    player_rotation takes an integer that represents the player id and returns
    an integer that shows the player after that player id
    '''

    # for a case where the player id is less than 3
    if player < 3:
        return player + 1

    # for a case where the player id is 3
    elif player == 3:
        return 0


def comb_checker(cards, phase):
    '''
    comb_checker takes two variables which are cards in the form of a nested
    list that represents a phase and phase is the intended type of phase
    for cards and comb_checker returns a boolean that shows whether the
    cards is the intended phase
    '''

    # for phase 1 and 3 checks both group sameness in values
    if phase == 1 or phase == 3:
        return same_checker(cards[0], 'Value') \
                and same_checker(cards[1], 'Value')

    # for phase 2, checks the group if they have the same suit
    elif phase == 2:
        return same_checker(cards[0], 'Suit')

    # for phase 4, checks the group if they are in a sequence
    elif phase == 4:
        return order_checker(cards[0])

    # for phase 5, checks both group
    # group 1 must have same colour and in a sequence
    # group 2 must be of the same value
    elif phase == 5:
        return (order_checker(cards[0]) and same_checker(cards[0], 'Color'))\
                and same_checker(cards[1], 'Value')


def phasedout_is_valid_play(play, player_id, table, turn_history, phase_status,
                            hand, discard):
    '''
    phasedout_is_valid_play takes variables named play which is a two element
    tuple representing the move, player_id which is an integer showing who is
    the player, table which is a list of two element tuples showing the phases
    of each players in one hand, turn_history which is a list of tuples showing
    all the moves to date in one hand, phase_status which is a list showing
    phase types that each players have completed, hand which is a list of
    player_id's cards, and discard which is a string showing the card on the
    top of the discard pile, the function returns a boolean to show if the move
    play is valid or not
    '''

    # checking the last move
    player, move = turn_history[-1]
    play_type, play_card = play
    fin_moves = []

    # the phase that the player_id is supposed to complete
    target_phase = phase_status[player_id] + 1

    # to make sure that it is player_id's turn
    if player_rotation(player) == player_id:
        cond = False

        # to make sure if the last player has discarded
        for turn_type, card in move:
            if turn_type == 5:
                cond = True
                break

        # if the last player has discarded, player_id must take a card
        if cond:
            if play_type == 1 or (play_type == 2 and discard == play_card):
                return True

    # if the last player in turn_history is player_id
    elif player == player_id:

        # iterate through the player_id's moves
        for turns, card in move:
            fin_moves.append(turns)

        # if player has not drawn a card
        if (play_type == 1 or play_type == 2) and 1 not in fin_moves \
        and 2 not in fin_moves:
            return True

        # if player wants to discard, they must have at least drawn a card
        elif play_type == 5 and (1 in fin_moves or 2 in fin_moves) \
        and 5 not in fin_moves:

            # to check if the discard card is in the hand
            if play_card in hand:
                return True

        # to check whether the player_id has completed a phase or not
        elif play_type == 3 and table[player_id][0] == None:

            # to flatten the nested list
            card_phase = [item for sublist in play_card for item in sublist]

            hand_copy = hand

            # iterate through the phase
            for card in card_phase:

                # removing the card in the hand so there will be no duplicates
                if card in hand_copy:
                    hand_copy.remove(card)
                else:
                    return False

            # to check the phase type
            play_phase = phasedout_phase_type(play_card)

            # to check if the phase type is correct
            return play_phase != None and play_phase == target_phase

        # to check if the phase has been completed
        elif play_type == 4 and table[player_id][0] != None:
            card, (target_player, target_group, target_index) = play_card

            # to check if the card is in the hand
            # to check if the index is correct
            if card in hand and \
            target_index + 1 - len(table[target_player][1][target_group]) < 2:

                # inserting the card to the intended target
                table[target_player][1][target_group].insert(
                    target_index, card)
                phase_type, cards = table[target_player]

                # checking if the phase type is still correct
                return comb_checker(cards, phase_type)

    return False


def possible_comb(hand, phase):
    '''
    possible_comb takes two variables, hand which is a list of cards in the
    form of a list and phase which is the targeted phase and it returns
    a list of possible phases depending on the targeted_phase or False
    if there are no possible phases from the hand
    '''

    possible_phase = []

    if phase == 1:

        # using combinations in hope to find two groups of sets of threes
        # so that there will be no overlap
        x = list(combinations(hand, 6))
        for a in x:

            # from each group, take combination of 3
            b = list(combinations(a, 3))
            for i in b:

                # test every group of 3
                if phasedout_group_type(i) == 1:

                    # if a group of 3 passed, it uses the group to remove
                    # elements from the original group of 6
                    y = [card for card in a if card not in i]

                    # if the other three elements from the original group
                    # passed, it is put onto a possible phase
                    if phasedout_group_type(y) == 1:
                        possible_phase.append([list(i), list(y)])

    elif phase == 2:

        # using combinations of 7 to find the group of same suits
        x = list(combinations(hand, 7))

        for poss in x:
            temp = []

            # if it pass the check it is added to possible phases
            if phasedout_group_type(poss) == 2:
                temp.append(list(poss))
                possible_phase.append(temp)

    elif phase == 3:

        # using combinations in hope to find two groups of sets of threes
        # so that there will be no overlap
        x = list(combinations(hand, 8))
        for a in x:

            # from each group, take combination of 4
            b = list(combinations(a, 4))
            for i in b:

                # test every group of 4
                if phasedout_group_type(i) == 3:

                    # if a group of 4 passed, it uses the group to remove
                    # elements from the original group of 8
                    y = [card for card in a if card not in i]

                    # if the other three elements from the original group
                    # passed, it is put onto a possible phase
                    if phasedout_group_type(y) == 3:
                        possible_phase.append([list(i), list(y)])

    elif phase == 4:
        scores = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '0': 10,
            'J': 11,
            'Q': 12,
            'K': 13
        }
        values = []

        # putting wilds and non-wilds in separate lists
        wilds = [card for card in hand if 'A' in card]

        # sorting the non-wilds by value and removing duplicates
        hand = sorted(
            list(set([card for card in hand if 'A' not in card])),
            key=lambda x: scores[x[0]])

        # to check if the non-wilds and wilds have a sum of at least 8
        if wilds != [] and len(hand) + len(wilds) >= 8:

            # generating possible locations for wilds
            indexes = list(
                combinations_with_replacement(range(len(hand)), len(wilds)))

            # iterate through the indexes
            for locations in indexes:

                # to avoid modifying the original hand
                hand_copy = copy.copy(hand)

                # inserting aces
                for index in range(len(locations)):
                    hand_copy.insert(locations[index], wilds[index])

                # slicing through every possibility
                for index in range(3):
                    temp = []

                    # testing the sliced list, if it passed it is added
                    # to possible phases
                    if phasedout_group_type(hand_copy[index:index + 8]) == 4:
                        temp.append(list(hand_copy[index:index + 8]))
                        possible_phase.append(temp)

        # if there are no wilds
        elif wilds == [] and len(hand) >= 8:
            hand_copy = copy.copy(hand)
            for index in range(3):
                temp = []

                # slicing through every possibility and testing it
                if phasedout_group_type(hand[index:index + 8]) == 4:
                    temp.append(hand_copy[index:index + 8])
                    possible_phase.append(temp)

    elif phase == 5:

        # red and black cards but with no suit, for easier removing duplicates
        red, blk = [], []

        # red and black cards with suit to later generate the original cards
        red_w_suit, blk_w_suit = [], []
        run_col = []

        # putting wilds and non_wilds in separate lists
        wilds = [card for card in hand if 'A' in card]
        no_wilds = [card for card in hand if card not in wilds]

        # splitting the non_wilds by colour
        for card in no_wilds:
            if card[-1] in ['C', 'S'] and card[0] not in blk:
                blk.append(card[0])
                blk_w_suit.append(card)
            elif card[-1] in ['H', 'D'] and card[0] not in red:
                red.append(card[0])
                red_w_suit.append(card)

        # if the red and the wilds are at least 4
        # also there should be at least 2 natural cards
        if len(red) + len(wilds) >= 4 and len(red) >= 2:

            # generating every index for aces
            indexes = list(
                combinations_with_replacement(range(len(red)), len(wilds)))

            # iterate through the indexes
            for location in indexes:

                # to avoid modifying the original
                red_test = copy.copy(red)

                # inserting aces
                for index in range(len(location)):
                    red_test.insert(location[index], wilds[index])
                i = 0
                while True:

                    # slicing through every possibility
                    x = red_test[i:i + 4]

                    # if the number of cards is less than 4, the loop breaks
                    if len(x) < 4:
                        break

                    # checking if it is in a sequence and that there are
                    # at least 2 natural cards
                    elif order_checker(x) and len(x) - wild_counter(x) >= 2:
                        y = []

                        # to generate cards with the suits
                        for val in x:

                            # if card is an ace it is added
                            if 'A' in val:
                                y.append(val)
                            else:
                                # iterate through the original cards
                                for card in red_w_suit:

                                    # if the value is the same, it is added
                                    # and the loop breaks
                                    if card[0] == val:
                                        y.append(card)
                                        break

                        # adding to the possible run of colour
                        run_col.append(y)
                    i += 1

        # if the black and the wilds are at least 4
        # also there should be at least 2 natural cards
        if len(blk) + len(wilds) >= 4 and len(blk) >= 2:

            # generating every index for aces
            indexes = list(
                combinations_with_replacement(range(len(blk)), len(wilds)))

            # iterate through the indexes
            for location in indexes:

                # to avoid modifying the original
                blk_test = copy.copy(blk)

                # inserting aces
                for index in range(len(location)):
                    blk_test.insert(location[index], wilds[index])
                i = 0
                while True:

                    # slicing through every possibility
                    x = blk_test[i:i + 4]

                    # if the number of cards is less than 4, the loop breaks
                    if len(x) < 4:
                        break

                    # checking if it is in a sequence and that there are
                    # at least 2 natural cards
                    elif order_checker(x) and len(x) - wild_counter(x) >= 2:
                        y = []

                        # to generate cards with the suits
                        for val in x:

                            # if card is an ace it is added
                            if 'A' in val:
                                y.append(val)

                            else:

                                # iterate through the original cards
                                for card in blk_w_suit:

                                    # if the value is the same, it is added
                                    # and the loop breaks
                                    if card[0] == val:
                                        y.append(card)
                                        break

                        # adding to the possible run of colour
                        run_col.append(y)
                    i += 1

        # iterate through the possible run of colour
        for runs in run_col:

            # using the possible run of colour to remove the elements of it
            # in hand
            sets = [card for card in hand if card not in runs]

            # creating possible set of same value
            poss_sets = list(combinations(sets, 4))

            # iterate through the possible sets of same value
            for i in poss_sets:

                # checking the set, if it passed, both the run and set
                # are added to possible phase
                if phasedout_group_type(i) == 3:
                    possible_phase.append([list(runs), list(i)])

    # function to flatten nested list
    flatten = lambda l: [item for sublist in l for item in sublist]

    # if there are possible phases, it returns the phase
    # if there are none, it returns False
    if flatten(possible_phase) != []:
        return possible_phase
    else:
        return False


def target_cards(discard, hand, comp_phase, target_phase, table):
    '''
    target_cards takes variables such as discard which is a string representing
    the card that is on the top of the discard pile, hand which is a list of
    the cards, comp_phase to show if a phase has been completed or not,
    target_phase which is an integer to show the phase that needs to be
    completed, and table which is a list of two element tuples which shows
    the phases on the table and the function returns a boolean to show
    if the discard is part of the cards that the player needs
    '''

    scores = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 10,
        'J': 11,
        'Q': 12,
        'K': 13
    }

    # getting the value and the suit of discard card
    val_dis, suit_dis = list(discard)

    # removing wilds and sorting hadn by value
    hand = [card for card in hand if 'A' not in card]
    hand = sorted(hand, key=lambda x: scores[x[0]])
    target = []

    # if the phase has not been completed
    if comp_phase == None:
        if target_phase == 1:

            # getting the number of cards based on the value
            values = dd(int)
            for val in hand:
                values[val[0]] += 1

            # the target would be any card that has at least 2 duplicates
            # of value
            target = [card[0] for card in hand if values[card[0]] > 1]

            # if there are duplicates, the target is any card with the same
            # value in the hand
            if max(values.values()) == 1 and target == []:
                target = list(values.keys())

            # to see if the value of discard is the target value
            return val_dis in target

        elif target_phase == 2:

            # getting the number of cards based on suits
            suits = dd(int)
            for val in hand:
                suits[val[-1]] += 1

            # the target would be any card with a suit and there has to be
            # at least three cards if that suit in the hand
            target = [suit[-1] for suit in hand if suits[suit[-1]] >= 3]

            # if there are no cards with at least 3 of the same suit
            # the target would be a suit on hand that has 2
            if max(suits.values()) <= 2 and target == []:
                target = [suit[-1] for suit in hand if suits[suit[-1]] == 2]

            # to see if the suit of the discard is in the target suit
            return suit_dis in target

        elif target_phase == 3:

            # getting the number of cards based on the value
            values = dd(int)
            for val in hand:
                values[val[0]] += 1

            # the target would be any card that has at least 3 duplicates
            # of value
            target = [card[0] for card in hand if values[card[0]] > 2]

            # if there are duplicates, the target is any card with the same
            # value in the hand if there are two of that value
            if max(values.values()) <= 2 and target == []:
                target = [x for x in values.keys() if values[x] == 2]

            # to check if the value of the discard is in the targeted value
            return val_dis in target

        elif target_phase == 4:
            cards = {
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '0': 0,
                'J': 0,
                'Q': 0,
                'K': 0,
                'A': 0
            }

            # to check how many cards there are based on value
            for val in hand:
                cards[val[0]] += 1

            # the target would be a card of any value that the player
            # does not have
            target = [i for i in cards.keys() if cards[i] == 0]

            # to check if the discard value is in what the target need
            return val_dis in target

        elif target_phase == 5:
            cards = {
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '0': 0,
                'J': 0,
                'Q': 0,
                'K': 0
            }

            # to check how many cards there are based on the value
            for val in hand:
                cards[val[0]] += 1

            # for the set, the target is any card of the same value if there
            # are at least 3
            target_set = [val for val in cards.keys() if cards[val] >= 3]

            # possible formed coloured run is from every cards owned
            col_run = [val for val in cards.keys() if cards[val] >= 1]
            target_run = []

            # iterate through the keys of value
            for val1 in cards.keys():

                # iterate through the keys of possible formed coloured run
                for val2 in col_run:

                    # generating every range from the cards in the
                    # possible coloured run
                    if scores[val2] - 1 <= scores[val1] <= scores[val2]+1\
                    and cards[val1] == 0 :
                        target_run.append(val1)

            target = target_run + target_set

            # to check if the discard value is the targeted discard
            return val_dis in target

    # if phase have been completed
    else:

        # iterate through every phases on the table
        for phase_type, phase in table:
            if phase_type == None:
                pass

            # for phase 1 or 3, the targeted card would be the values of
            # each group
            elif phase_type == 1 or phase_type == 3:
                for i in phase:
                    if 'A' not in i:
                        target.append(i[0])
                        break

            # for phase 2, the targeted card would be the suit
            elif phase_type == 2:
                group = phase[0]
                for i in group:
                    if 'A' not in i:
                        target.append(i[-1])
                        break
            # for phase 4, the targeted card would the value before the card
            # in first index and after the card in the last index
            elif phase_type == 4:
                group = phase[0]

                # to avoid wilds if the first and last indexes
                for i in range(len(group)):
                    if 'A' not in group[i]:
                        first_card_score = scores[group[i][0]] - i - 1
                        break

                group_rev = group[::-1]

                for i in range(len(group_rev)):
                    if 'A' not in group_rev[i]:
                        last_card_score = scores[group_rev[i][0]] + i + 1
                        break

                # getting the target values
                target = [
                    val for val in scores.keys()
                    if scores[val] == first_card_score or
                    scores[val] == last_card_score
                ]

            # for phase 5, it depends on the group
            elif phase_type == 5:
                # group 1 is a coloured run and group 2 is a value set
                run_col = phase[0]
                set_val = phase[-1]

                # for the value, just find the value adn add it to target
                for val in set_val:
                    if val[0] != 'A':
                        target.append(val[0])
                        break

                # to avoid aces in the first and last indexes
                for index in range(len(run_col)):
                    if 'A' not in run_col[index]:
                        first_card_score = scores[run_col[index][0]] - index - 1
                        break

                run_rev = run_col[::-1]
                for index in range(len(run_rev)):
                    if 'A' not in run_rev[index]:
                        last_card_score = scores[run_rev[index][0]] + index + 1
                        break

                # the target would be any card with the value directly below
                # or higher than the cards in the first index and the last index
                # respectively and also of the same colour
                target = [
                    val for val in scores.keys()
                    if scores[val] == first_card_score or
                    scores[val] == last_card_score
                ]

        # to check if the value or the suit of the discard is needed
        return val_dis in target or suit_dis in target


def discards(hand, phase_target, comp_phase):
    '''
    discards take thre variables which are hand which is a list of cards,
    phase_target which is an integer showing what the phase that player
    need to complete and comp_phase which shows if the player has completed
    a phase or not
    '''
    discard = []

    # putting wilds and non-wilds in two separate lists
    wilds = [card for card in hand if 'A' in card]
    no_wilds = [card for card in hand if card not in wilds]
    scores = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 10,
        'J': 11,
        'Q': 12,
        'K': 13
    }

    # if the phase have not been completed
    if comp_phase == None:

        if phase_target == 1:
            values = dd(int)

            # getting the number of cards based on value
            for val in hand:
                values[val[0]] += 1

            # getting all the cards that has no duplicates and sorting it by
            # value
            discard = [card for card in no_wilds if values[card[0]] < 2]
            discard = sorted(discard, key=lambda x: scores[x[0]])

        elif phase_target == 2:
            suits = dd(int)

            # getting the number of cards based on suit
            for suit in hand:
                suits[suit[-1]] += 1

            # getting all the cards that has duplicates less than 4
            # and sorting it by value
            discard = [card for card in no_wilds if suits[card[-1]] < 4]
            discard = [
                card for card in discard
                if suits[card[-1]] == min(suits.values())
            ]
            discard = sorted(discard, key=lambda x: scores[x[0]])

        elif phase_target == 3:

            # getting the number of cards based on value
            values = dd(int)
            for val in hand:
                values[val[0]] += 1

            # getting all the cards that has duplicates less than 3
            # sorting it by how many the cards there are first
            # and then the value
            discard = [card for card in no_wilds if values[card[0]] < 3]
            discard = sorted(
                discard,
                key=lambda x: (values[x[0]], scores[x[0]]),
                reverse=True)

        elif phase_target == 4:

            # counting the cards based on value
            values = dd(int)
            for val in hand:
                values[val[0]] += 1

            # discard are cards that has duplicates
            discard = [card for card in no_wilds if values[card[0]] > 1]

            # reversing the order to get the highest value
            no_wilds = no_wilds[::-1]
            if discard == []:
                wild = len(wilds)

                # counting the gap between each values
                for index in range(len(no_wilds) - 1):

                    # if the gap is too high that aces can not cover
                    # it added it to the discard
                    gap = (scores[no_wilds[index][0]] -
                           scores[no_wilds[index + 1][0]])
                    if wild - gap + 1 < 0:
                        wild = wild - gap + 1
                    else:
                        discard.append(no_wilds[index])

            # it sorts by the most many duplicates and then value
            discard = sorted(
                discard, key=lambda x: (values[x[0]], scores[x[0]]))

        elif phase_target == 5:
            values = dd(int)
            colors = {'C': 'Black', 'S': 'Black', 'D': 'Red', 'H': 'Red'}
            col = ([], [])

            # counting how many cards there are and puting red cards and
            # black cards in its own lists
            for card in no_wilds:
                values[card[0]] += 1
                if colors[card[-1]] == 'Red' and card[-1] not in col[0]:
                    col[0].append(card[0])
                elif colors[card[-1]] == 'Black' and card[-1] not in col[-1]:
                    col[-1].append(card[0])

            red, blk = col
            red_gap, blk_gap = 0, 0

            # counting the gap, the color with higher gap gets discarded
            for i in range(len(red) - 1):
                red_gap = red_gap + scores[red[i + 1]] - scores[red[i]]
            for j in range(len(blk) - 1):
                blk_gap = blk_gap + scores[blk[j + 1]] - scores[blk[j]]

            if red_gap > blk_gap:
                discard = [card for card in no_wilds if card[0] in red]
            elif blk_gap > red_gap:
                discard = [card for card in no_wilds if card[0] in blk]
            else:
                discard = []

            # adding the discards from the color and those that has duplicates
            # of exactly two
            discard = discard + [
                card for card in no_wilds if values[card[0]] == 2
            ]

            discard = sorted(discard, key=lambda x: scores[x[0]])

        if discard != []:
            return discard[-1]
        else:
            return max(no_wilds, key=lambda x: scores[x[0]])
    else:
        return max(no_wilds, key=lambda x: scores[x[0]])


def move4(table, hand):
    '''
    move4 takes two variables table which is a list of two tuple elements
    which shows the phases on the table and variable hand which is a list
    of cards, move 4 return a two element tuple which are a card and a three
    element tuple with integers that shows the player, the group of the phase
    and the index of the phase
    '''

    # iterate through the cards in hand
    for card in hand:
        for target_player in range(len(table)):
            phase, cards = table[target_player]

            if phase != None:

                # iterate through the index
                for target_group in range(len(cards)):

                    # copying hand to avoid modifying the original
                    first = copy.deepcopy(cards)
                    last = copy.deepcopy(cards)

                    # the possible indexes are the first adn the last
                    index1 = 0
                    index2 = len(last[target_group])

                    # adding the card in first and last index
                    first[target_group].insert(0, card)
                    last[target_group].insert(len(last[target_group]), card)

                    # checking if even after added, the card still follow
                    # the rules of the group
                    if comb_checker(first, phase):
                        return card, (target_player, target_group, index1)
                    elif comb_checker(last, phase):
                        return card, (target_player, target_group, index2)


def phasedout_play(player_id, table, turn_history, phase_status, hand,
                   discard):
    '''
    phasedout_play takes variables such as player_id which is an integer
    representing the player, table which is a list of two element tuple,
    phase_status which is a list of phases completed by players, hand which
    is a list of cards, discard which is a string representing the top card
    on the discard pile
    '''

    # getting the information of the last player
    if turn_history != []:
        player, moves = turn_history[-1]
    else:
        player, moves = None, None

    scores = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 25
    }

    # sorting the hand by value
    hand = sorted(hand, key=lambda x: scores[x[0]])

    # show whether player_id has completed a phase or not
    comp_phase = table[player_id][0]

    # if player_id has not completed a phase, target_phase is set
    if comp_phase == None:
        target_phase = phase_status[player_id] + 1
    else:
        target_phase = None

    # if the last player is not player_id, player_id must draw
    if player != player_id:

        # using the function to determine if player_id should draw from discard
        target = target_cards(discard, hand, comp_phase, target_phase, table)

        # if discard is useful or an ace in discard pile, player_id draw from
        # discard, otherwise player_id draws from the deck
        if target or 'A' in discard:
            return (2, discard)
        else:
            return (1, None)

    # if the phase has not been completed, it will try to find a phase
    # from the hand
    if comp_phase == None:
        phases = possible_comb(hand, target_phase)
        if phases:

            # a function of phase scores
            cards_score = {}

            # a function to flatten nested lists
            flatten = lambda l: [item for sublist in l for item in sublist]

            # counting the phase scores
            for possibles in phases:
                cards_score[phasedout_score(flatten(possibles))] = possibles

            result = cards_score[max(cards_score)]

            # returning the phase with the highest score
            return 3, result

    # to generate possibilities of putting card in someone's phase
    put_on_phase = move4(table, hand)

    # to check if there is a possibility to put a card in someone's phase
    # and that player_id has completed a phase
    if put_on_phase != None and comp_phase != None:
        return 4, put_on_phase

    # if there are no more possible moves, the player discard a card
    else:
        dis = discards(hand, target_phase, comp_phase)
        return 5, dis
