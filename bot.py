import discord
from botSecret import secret
from fetch import *
from data import *
from discord.ext import commands
import random
from collections import namedtuple
import asyncio
import time
import aiohttp

import json


# Set coin specific parameters


MaxCoinFlipBet = 10 # Enter the max bet amount for coinflip
MinCoinFlipBet = 1 # Enter the min bet amount for coinflip
MaxBlackJackBet = 10 # Enter the max bet amount for blackjack
MinBlackJackBet = 1 # Enter the min bet amount for blackjack
MaxDiceBet = 10 # Enter the max bet amount for dice
MinDiceBet = 1 # Enter the min bet amount for dice
LostBetsAddy = "FQUv8z29dJHCuQojJo5XkGUFYYyKgGDT6g" # Enter the address the client would like lost bets to be sent to
myUid = "FQUv8z29dJHCuQojJo5XkGUFYYyKgGDT6g" # Enter the account name for the address the client would like to pay out wins from

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Bot is online!")
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="$help"))


@bot.command()
async def help(ctx):
    tuid = "<@" + str(ctx.author.id) + ">"
    await ctx.channel.send(tuid + """
    \n**$send** - Sends coins to any address. Example: ' $send Cca1eNQMF4JYCjzBsbJBbLLHE2jDPmqzop 1 '
    \n**$create** - Creates a wallet attached to your discord account.
    \n**$balance** - Check your wallet balance.
    \n**$casino** - Check the Casino Payout wallet balance.
    \n**$address** - Returns the users Wallet address.
    \n**$coinflip** - Starts a game of coinflip. Example: ' $coin 1 Heads ' where 1 is the amount you wish to bet.
    \n**$blackjack** - Starts a game of blackjack. Example: ' $jack 10 ' where 10 is the amount you wish to bet.
    \n**$dice** - Starts a game of dice. Example: ' $dice 10 6 ' where 10 is the amount you wish to bet and 6 is the amount to roll under in order to win.
    \n**$payouts** - Returns a list of payouts for Dice depending on what the 'under' is set at.
    """)

@bot.command()
async def payouts(ctx):
    tuid = "<@" + str(ctx.author.id) + ">"
    await ctx.channel.send(tuid + """
    ```\n**Dice Payouts:**
    \nUnder 11 Payout = 1.02 * Bet
    \nUnder 10 Payout = 1.05 * Bet
    \nUnder 9 Payout = 1.2 * Bet
    \nUnder 8 Payout = 1.45 * Bet
    \nUnder 7 Payout = 1.75 * Bet
    \nUnder 6 Payout = 2 * Bet
    \nUnder 5 Payout = 2.35 * Bet
    \nUnder 4 Payout = 2.75 * Bet
    \nUnder 3 Payout = 3.5 * Bet
    \nSnake Eyes Payout = 4 * Bet```
    """)

# Create User Wallet
@bot.command()
async def create(ctx):

    raw = str(ctx.author.id)
    uid = "<@" + str(ctx.author.id) + ">"


    address = getAddress(str(ctx.author.id))
    balance = getBalance(str(ctx.author.id))
    username = str(ctx.author)
    botMessage = await ctx.channel.send(uid + ' ' + '\n**AltCasino Wallet - CHANGEME ** \n**Address:** '
                                   + str(address) + ' \n**Balance:** ' + str(balance))

    time.sleep(5)

    await ctx.message.delete()
    return

# Return User Balance
@bot.command()
async def balance(ctx):

    uid = "<@" + str(ctx.author.id) + ">"

    newBalance = getBalance(str(ctx.author.id))
    botMessage = await ctx.channel.send(uid + ' ' + '\n**AltCasino Wallet - CHANGEME** \n**Balance:** ' + str(newBalance) + ' CHANGEME')

    time.sleep(5)
    await botMessage.delete()
    await ctx.message.delete()
    return

    # Return User Balance
@bot.command()

async def casino(ctx):

    uid = "<@" + str(ctx.author.id) + ">"

    newBalance = getMainBalance()
    botMessage = await ctx.channel.send(uid + ' ' + '\n**AltCasino Main Payout Wallet - CHANGEME** \n**Balance:** ' + str(newBalance) + ' CHANGEME')

    time.sleep(1)

    await ctx.message.delete()
    return


# Return User Deposit Address
@bot.command()

async def address(ctx):


    uid = "<@" + str(ctx.author.id) + ">"

    userAddy = getNewAddy(str(ctx.author.id))

    print(userAddy)
    botMessage = await ctx.channel.send(uid + '\n**AltCasino Wallet - CHANGEME**' + '\n**Wallet Address:** ' + userAddy)
    time.sleep(5)
    await botMessage.delete()
    await ctx.message.delete()
    return


# Send Coins
@bot.command()
async def send(ctx, arg1, arg2):
    tuid = uid = "<@" + str(ctx.author.id) + ">"
    uid = str(ctx.author.id)
    address = str(arg1)
    amount = str(arg2)
    spend = sendCoins(uid, address, amount)
    print(spend)


    botMessage = await ctx.channel.send(tuid + "\nTransaction Successful: \n**TXID:** " + str(spend))
    time.sleep(5)
    await botMessage.delete()
    await ctx.message.delete()
    return

# Start a Game of Coinflip
@bot.command()
async def coinflip(ctx, bet, userChoice):

    uid = str(ctx.author.id)
    tuid = "<@" + str(ctx.author.id) + ">"


    userAddy = getNewAddy(str(ctx.author.id))
    toPlay = getBalance(str(ctx.author.id))
    newBalance = toPlay

    if newBalance < float(bet):
        botMessage = await ctx.channel.send(tuid + "\nSorry, you don't have that many coins. \n**Balance:** " + str(newBalance) + ' CHANGEME')
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return
    elif float(bet) > MaxCoinFlipBet:
        botMessage = await ctx.channel.send(tuid + "\nSorry, the max bet for Coinflip is " + str(MaxCoinFlipBet) + ' CHANGEME')
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return
    elif float(bet) < MinCoinFlipBet:
        botMessage = await ctx.channel.send(tuid + "\nSorry, the minimum bet for Coinflip is " + str(MinCoinFlipBet) + ' CHANGEME')
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return
    elif newBalance >= float(bet):
        betOn = userChoice.lower()
        Heads = "heads"
        Tails = "tails"
        options = [Heads, Tails, Heads, Tails, Heads, Tails, Heads, Tails, Heads, Tails, Heads, Tails, Heads, Tails, Heads, Tails, Heads, Tails]
        landed = random.choice(options)

        if landed == betOn:
            botMessage1 = await ctx.channel.send(tuid + "\nCoin landed on **" + landed.upper() + "**" + "\n**Congratulations!** You Won " + str(bet) + ' CHANGEME')
            txid = sendCoins(myUid, userAddy, bet)
            botMessage = await ctx.channel.send(txid + " - txid")
            botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
            botMessage = await ctx.channel.send("**Please wait a few minutes before checking your balance again!**")
            time.sleep(5)


            await ctx.message.delete()
            await ctx.channel.purge(limit=3)
            await ctx.channel.send("**You can now place a new bet**")
            return

        elif landed != betOn:
            botMessage1 = await ctx.channel.send(tuid +"\nCoin landed on **" + landed.upper() + "**" + "\n**Oops!** You Lost " + str(bet) + ' CHANGEME')
            sendCoins(uid, LostBetsAddy, bet)

            botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
            time.sleep(5)
            await botMessage.delete()
            await botMessage1.delete()
            await ctx.message.delete()
            await ctx.channel.purge(limit=3)
            await ctx.channel.send("**You can now place a new bet**")
            return
    return

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

async def get_input_of_type(func, ctx):
    while True:
        try:
            msg = await bot.wait_for('message', timeout= 30, check=check(ctx))
            return func(msg.content)
        except ValueError:
            continue

# Start a game of BlackJack
@bot.command()
async def blackjack(ctx, bet):
    userAddy = getNewAddy(str(ctx.author.id))
    toPlay = getBalance(str(ctx.author.id))
    newBalance = toPlay
    Ace = False
    tuid = "<@" + str(ctx.author.id) + ">"

    if float(bet) > MaxBlackJackBet:
        botMessage = await ctx.channel.send(tuid + "\nSorry, Max bet for Black Jack is " + str(MaxBlackJackBet) )
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return

    elif float(bet) < MinBlackJackBet:
        botMessage = await ctx.channel.send(tuid + "\nSorry, Minimum bet for Black Jack is " + str(MaxBlackJackBet) )
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return

    if newBalance < float(bet):
        botMessage = await ctx.channel.send(tuid + "\nSorry, you don't have that many coins. \n**Balance:** "
        + str(newBalance) + ' ' + CoinName)
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return

    uid = str(ctx.author.id)

    userAddy = getNewAddy(str(ctx.author.id))

    cValue = {'Ace': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
              'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
    cSuit = {'Hearts': 0, 'Spades': 1, 'Clubs': 2, 'Diamonds': 3,
              'Hearts': 4, 'Spades': 5, 'Clubs': 6, 'Diamonds': 7,
              'Hearts': 8, 'Spades': 9, 'Clubs': 10, 'Diamonds': 11,
              'Hearts': 12, 'Spades': 13, 'Clubs': 14, 'Diamonds': 15,
              'Hearts': 16, 'Spades': 17, 'Clubs': 18, 'Diamonds': 19,
              'Hearts': 20, 'Spades': 21, 'Clubs': 22, 'Diamonds': 23}
    deck = [] # Empt Deck Array
    dCards = [] # Empty Dealer Cards Array
    pCards = [] # Empty Player Cards Array

    # Build Deck
    for i in cValue.keys():
        for j in cSuit.keys():
            deck.append(i + ' of ' + j) # Adds 52 cards to the Deck Array

    # Shuffle Deck
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)
    # Dealer Hand

    while len(dCards) != 2:
        dCards.append(random.choice(deck)) # Picks Random Cards from the deck and places them into the Dealers Hand

    if len(dCards) == 2:
        dFirstCard = getCardValue(dCards[0])

        dSecondCard = getCardValue(dCards[1])

        dealerTotal = dFirstCard + dSecondCard

    if getCardValue(dCards[0]) == 1:
        dealerTotal = dealerTotal + 10

        #Check if dealer has Ace as first cards, if so, Ace = 11 - If 2 Aces are drawn, total is 12
    if getCardValue(dCards[1]) == 1:
        dealerTotal = dealerTotal + 10
    if dealerTotal == 22:
        dealerTotal = 12
    while len(pCards) != 2:
        pCards.append(random.choice(deck)) # Picks Random Cards from the deck and places them into the Players Hand

    if len(pCards) == 2:
        pFirstCard = getCardValue(pCards[0]) # Returns card's numerical value
        pSecondCard = getCardValue(pCards[1])
        playerTotal = pFirstCard + pSecondCard # Sum of Players first and second card

    if getCardValue(pCards[0]) == 1:
        playerTotal += 10
        Ace = True
        #Check it player has Ace as first 2 cards, if so, Ace = 11 - If 2 Aces are drawn, total is 12

    if getCardValue(pCards[1]) == 1:
        playerTotal += 10
        Ace = True
    if playerTotal == 22:
        playerTotal = 12
    # Determine if user wants to Hit or Stay
    if playerTotal < 21:
        botMessage = await ctx.channel.send(tuid + "\nDealer Has **HIDDEN** & " + '**' + dCards[0] + '**'
        + "\nYou Have " + '**' + str(pCards) + '**' + ' :** ' + str(playerTotal) + '**'
        + "\n**Stay**: [S] or **Hit**: [H]?")
        stayOrHit = await get_input_of_type(str, ctx)

        while stayOrHit.lower() != "h" and stayOrHit.lower() != "s":
            botMessage = await ctx.channel.send(tuid + "\n Please enter **Stay**: [S] or **Hit**: [H]")
            stayOrHit = await get_input_of_type(str, ctx)


        while stayOrHit.lower() == "h":
            pCards.append(random.choice(deck))
            cardNum = len(pCards)
            cardNum -= 1
            newCard = getCardValue(pCards[cardNum])

            playerTotal += newCard
            if Ace == True and playerTotal > 21:
                playerTotal -= 10

            if getCardValue(pCards[cardNum]) == 1 and (playerTotal + 10) <= 21:
                playerTotal += 10

            if getCardValue(pCards[cardNum]) == 1 and (playerTotal + 10) >= 22:

                playerTotal = playerTotal

            botMessage = await ctx.channel.send(tuid + "\nDealer Has **HIDDEN** & " + '**' + dCards[0] + '**'
             + "\nYou Have " + '**' + str(pCards) + '**' + ' : **' + str(playerTotal) + '**' + "\n**Stay**: [S] or **Hit**: [H]?")





           # if Player hit and hasn't busted ask player to Stay or Hit
            if playerTotal <= 21:
                stayOrHit = await get_input_of_type(str, ctx)
                while stayOrHit.lower() != "h" and stayOrHit.lower() != "s":
                    botMessage = await ctx.channel.send(tuid + "\n Please enter **Stay**: [S] or **Hit**: [H]")
                    stayOrHit = await get_input_of_type(str, ctx)



           # Determine if Player Hit and hasn't busted
            elif playerTotal > 21:
                botMessage = await ctx.channel.send(tuid + "\nBust! You Lost " + str(bet) + ' CHANGEME \nYour Total: **' + str(playerTotal) + '**')
                sendCoins(uid, LostBetsAddy, bet)

                botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
                time.sleep(5)

                botMessage = await ctx.channel.send("You can now place a new bet.")
                return

        # If Decision does not equal hit
        # TODO switch this to a more explicit method, setting it equal to Stay causes random infinite loops
        # It's currently fixed by not allowing input other than stay or hit
        while stayOrHit.lower() != "h":

            # If Dealer hand is less than 16, Dealer draws another card
            mytotal = dealerTotal
            if dealerTotal <= 16:
                dCards.append(random.choice(deck))
                DcardNum = len(dCards)
                DcardNum -= 1
                newDCard = getCardValue(dCards[DcardNum])

                dealerTotal += newDCard
            if (dealerTotal - mytotal) == 1 and (dealerTotal + 10) <= 21:
                dTotal = dTotal + 10
                dealerTotal = dTotal
            if (dealerTotal - mytotal) == 1 and (dealerTotal + 10) >= 22:
                dealerTotal = dealerTotal





            # Determine if Dealer Hand Busted
            elif dealerTotal > 21:
                botMessage = await ctx.channel.send(tuid + "\nDealer Has " + '**' + str(dCards) + '**'
                    + "\nYou Have " + '**' + str(pCards) + '**' + ' : **' + str(playerTotal) + '**')
                botMessage = await ctx.channel.send(tuid + "\nYou Won! " + str(bet) + " CHANGEME \nDealer Busted" + '\nYour Total: ' '**' + str(playerTotal) + '** \nDealer Total: **' + str(dealerTotal) + '**')
                sendCoins(myUid, userAddy, bet)

                botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
                time.sleep(5)

                botMessage = await ctx.channel.send("You can now place a new bet.")
                return

            # Determine Winner
            elif dealerTotal > 16 and dealerTotal <= 21:
                if dealerTotal < playerTotal:
                    botMessage = await ctx.channel.send(tuid + "\nDealer Has " + '**' + str(dCards) + '**'
                    + "\nYou Have " + '**' + str(pCards) + '**' + ' : **' + str(playerTotal) + '**')
                    botMessage = await ctx.channel.send(tuid + "\nYou Won! "  + str(bet) + ' CHANGEME \nYour Total: ' '**' + str(playerTotal) + '** \nDealer Total: **' + str(dealerTotal)+ '**')
                    sendCoins(myUid, userAddy, bet)

                    botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
                    time.sleep(5)

                    botMessage = await ctx.channel.send("You can now place a new bet.")
                    return
                elif dealerTotal > playerTotal:
                    botMessage = await ctx.channel.send(tuid + "\nDealer Has " + '**' + str(dCards) + '**'
                    + "\nYou Have " + '**' + str(pCards) + '**' + ' : **' + str(playerTotal) + '**')
                    botMessage = await ctx.channel.send(tuid + "\nYou Lost! "  + str(bet) + ' CHANGEME \nYour Total: ' '**' + str(playerTotal) + '** \nDealer Total: **' + str(dealerTotal) + '**')
                    sendCoins(uid, LostBetsAddy, bet)

                    botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
                    time.sleep(5)

                    botMessage = await ctx.channel.send("You can now place a new bet.")
                    return

            # Determine A Tie
            if playerTotal == dealerTotal and playerTotal <= 21 and dealerTotal <= 21:
                botMessage = await ctx.channel.send(tuid + "\nDealer Has " + '**' + str(dCards) + '**'
                    + "\nYou Have " + '**' + str(pCards) + '**' + ' : **' + str(playerTotal) + '**')
                botMessage = await ctx.channel.send(tuid + "\nTie! No Payout " + '\nYour Total: ' '**' + str(playerTotal) + '** \nDealer Total: **' + str(dealerTotal) + '**')
                updateBalances()
                botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
                time.sleep(5)

                botMessage = await ctx.channel.send("You can now place a new bet.")
                return


# Start a game of Dice
@bot.command()
async def dice(ctx, bet, under):
    tuid = "<@" + str(ctx.author.id) + ">"
    uid = str(ctx.author.id)

    userAddy = getNewAddy(str(ctx.author.id))
    toPlay = getBalance(str(ctx.author.id))
    newBalance = toPlay

    if newBalance < float(bet):
       botMessage = await ctx.channel.send(tuid + "\nSorry, you don't have that many coins. \n**Balance:** "
        + str(newBalance) + ' CHANGEME')
       time.sleep(5)
       await botMessage.delete()
       await ctx.message.delete()
       return

    elif float(bet) > MaxDiceBet:
        botMessage = await ctx.channel.send(tuid + "\nSorry, the max bet for Dice is " + str(MaxDiceBet) + ' CHANGEME')
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return
    elif float(bet) < MinDiceBet:
        botMessage = await ctx.channel.send(tuid + "\nSorry, the minimum bet for Dice is " + str(MinDiceBet) + ' CHANGEME')
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return


    userAddy = getNewAddy(str(ctx.author.id))


    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    roll = dice1 + dice2


    if int(under) == 2:
        payout = float(bet) * 4
    if int(under) == 3:
        payout = float(bet) * 3.5
    if int(under) == 4:
        payout = float(bet) * 2.75
    if int(under) == 5:
        payout = float(bet) * 2.35
    if int(under) == 6:
        payout = float(bet) * 1.2
    if int(under) == 7:
        payout = float(bet) * 1.75
    if int(under) == 8:
        payout = float(bet) * 1.45
    if int(under) == 9:
        payout = float(bet) * 1.2
    if int(under) == 10:
        payout = float(bet) * 1.05
    if int(under) == 11:
        payout = float(bet) * 1.02


    elif int(under) > 11:
        botMessage = await ctx.channel.send(tuid + "\nRoll Under value must be less than or equal to 11. ")
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return
    elif int(under) < 2:
        botMessage = await ctx.channel.send(tuid + "\nRoll Under value must be greater than or equal to 3. ")
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        return

    if roll == 2 and int(under) == 2:
        botMessage = await ctx.channel.send(tuid + "\n**Snake Eyes!** \n**You Won " + str(payout) + ' CHANGEME**' +
        "\nDice One: " + str(dice1) + "\nDice Two: " + str(dice2) + "\n**Total:** " + str(roll))
        sendCoins(myUid, userAddy, payout)

        botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        botMessage = await ctx.channel.send("You can now place a new bet.")
        await ctx.channel.purge(limit=3)
        return

    elif roll < int(under):
        botMessage = await ctx.channel.send(tuid + "\n**You Won " + str(payout) + ' CHANGEME**' +
        "\nDice One: " + str(dice1) + "\nDice Two: " + str(dice2) + "\n**Total:** " + str(roll))
        sendCoins(myUid, userAddy, payout)

        botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        await ctx.channel.purge(limit=3)
        botMessage = await ctx.channel.send("You can now place a new bet.")
        return

    elif roll >= int(under):
        botMessage = await ctx.channel.send(tuid + "\n**You Lost " + str(bet) + ' CHANGEME**' +
        "\nDice One: " + str(dice1) + "\nDice Two: " + str(dice2) + "\n**Total:** " + str(roll))
        sendCoins(uid, LostBetsAddy, bet)

        botMessage = await ctx.channel.send("**Please wait 5 seconds before placing a new bet**")
        time.sleep(5)
        await botMessage.delete()
        await ctx.message.delete()
        await ctx.channel.purge(limit=3)
        botMessage = await ctx.channel.send("You can now place a new bet.")
        return





bot.run(secret)
