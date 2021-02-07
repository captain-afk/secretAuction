import json
import os

# TODO: error handling. If you try to place a bid and the file is empty, it will not be happy... I do not check input for valid anything...

def addItem(itemName):                          # adds a new item for auction to auction.json
    with open("auction.json") as json_file:
        data = json.load(json_file)

    item = {
        "name": itemName,
        "bids": []
    }
    data["items"].append(item)

    with open("auction.json", 'w') as outfile:
        json.dump(data, outfile)
    return()

def listItems():                                # loops through and makes a list of all items up for auction
    itemList = []
    with open("auction.json") as json_file:
        data = json.load(json_file)
    for x in data["items"]:
        itemList.append(x['name'])
    return(itemList)

def hasExistingBid(biddingOnitemIndex,username,data):   # Checks if user has an existing bid or not
    exists = False
    indexOfBid = 0
    for user in data["items"][biddingOnitemIndex]["bids"]:
        if user['user'] == username:
            exists = True
            break
        indexOfBid += 1
    return(exists,indexOfBid)
    

def bidItem(bidAmount,biddingOnItem,userName):  # Checks if the user already has a bid, if so updates it in auction.json
    with open("auction.json") as json_file:     # otherwise adds a fresh bid to the item in auction.json
        data = json.load(json_file)

    bid = {
        "user":userName,
        "bid": int(bidAmount)
    }
    index = 0
    foundIt = False
    for x in data["items"]:
        if biddingOnItem == x['name']:
            foundIt = True
            break
        else:
            index += 1
    if foundIt == True:
        HasExistingBid,indexOfBid = hasExistingBid(index,userName,data)
        if HasExistingBid == False:
            data["items"][index]["bids"].append(bid)
            with open("auction.json", 'w') as outfile:
                json.dump(data, outfile)
        else:
            data["items"][index]["bids"][indexOfBid]["bid"] = int(bidAmount)
            print("Updating existing bid")
            with open("auction.json", 'w') as outfile:
                json.dump(data, outfile)
    return()

def resetFile():                                # resets auction.json back to having no bids and no items
    data = {
        "items": []
    }
    with open("auction.json", 'w') as outfile:
                json.dump(data, outfile)
    return()

def revealWinner(revealedItem):                 # loads file, loops through all the items until it finds the correct item.
    with open("auction.json") as json_file:     # Then loops through the bids to find the highest bidder. Returns winner and bid amount
        data = json.load(json_file)
    
    itemIndex = 0
    bidIndex = -1       # -1 as a cludge as I am adding 1 more than I should do the index in the end
    highestBid = 0

    for item in data["items"]:
        if item["name"] == revealedItem:
            for bid in data["items"][itemIndex]["bids"]:
                currentBid = bid["bid"]
                if currentBid > highestBid:
                    highestBid = currentBid
                bidIndex += 1
            break
        itemIndex += 1

    winner = data["items"][itemIndex]["bids"][bidIndex]["user"]
    winningAmount = data["items"][itemIndex]["bids"][bidIndex]["bid"]

    return(winner,winningAmount)

def main():
    print("Welcome to the secret Auction!")
    print("What would you like to do?: 'add' an item to bid on, 'bid' on an item, 'reveal' the winner of an auction, or 'reset' everything?")
    userCommand = input()
    if userCommand.lower() == "add":
        print("What would you like to add to the auction?")
        newItem = input()
        addItem(newItem)

    elif userCommand.lower() == "bid":
        print("what is your name?")
        userName = input()
        itemList = listItems()
        print("What would you like to bid on?")
        print(itemList)
        biddingOnItem = input()
        print("How much are you betting?")
        bidAmount = input()
        bidItem(bidAmount,biddingOnItem,userName)

    elif userCommand.lower() == "reveal":
        itemList = listItems()
        print("Which item do you want to reveal the winner of?")
        print(itemList)
        revealedItem = input()
        winner,winningAmount = revealWinner(revealedItem)
        print(winner,"Won with a bid of",winningAmount)

    elif userCommand.lower() == "reset":
        print("Are you sure you want to blow away all existing bid items and bids? y/n")
        confirmation = input()
        if confirmation == 'y':
            print("Alright, blank slate time")
            resetFile()
main()