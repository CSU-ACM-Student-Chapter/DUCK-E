'''
Author: Karina Cabrera
Description: Web Filter Class
Note:Another Class should be in charge of messages if fun has_SafeMsgLinks rturns false
'''
import re
class Website_Filter():

    @classmethod
    def __init__(self):
        pass

    @classmethod
    def has_website(self,txt) -> list:
        '''Seperates websites from user string, returns empty if no websites are found'''
        status = re.findall('[A-Za-z]+\.[A-za-z]{2,3}(?![A-Za-z])', txt)
        return status

    @classmethod
    def has_approvedTLD(self,Web_Link) -> bool:
        '''Checks if website contains an approved top-level domain, returns false if not'''
        status = bool(re.search('[^\s]+\.(gov|edu|org).*', Web_Link))
        return status

    @classmethod
    def has_approvedTLD_List(self,WebLink_List) -> list:
        '''Iterates through each link checking TLD, returns list of links that violate function: has_approvedTLD'''
        nonApprovedLinks = []
        for i in WebLink_List:
            if(not Website_Filter.has_approvedTLD(i)):
                nonApprovedLinks.append(i)
        return nonApprovedLinks

    @classmethod
    def is_Whitelist_Match(self, Whitelist, str) -> bool:
        '''Checks if str matches with links inside Whitelist'''
        Web_Txt = open(Whitelist)
        Web_List = Web_Txt.readlines()
        for i in Web_List:
            cleaned = i.rstrip()
            if (str == cleaned):
                return True
        return False

    @classmethod
    def is_total_Whitelist_Match(self,Whitelist, mylist) -> bool:
        '''Loops through link list, checks if links match with whitelist, returns false if any do not match'''
        for i in mylist:
            link_Status = Website_Filter.is_Whitelist_Match(Whitelist,i)
            if (not link_Status):
                return False
        return True

    @classmethod
    def has_SafeMsgLinks(self,file_WhiteList,msg_String) -> bool:
        '''Filters input msg for links. If msg contains unapproved links returns false '''
        WebList = Website_Filter.has_website(msg_String)
        if(len(WebList) == 0 ):
            #If msg does not contain website, return true as safe msg
            return True
        else:
            #If msg contains websites for approved TLD
            #todo: rename has approved tld to has_unapproved tld
            unapproved_TLD = Website_Filter.has_approvedTLD_List(WebList)
            #If msg contains unapproved TLD's check whitelist
            if(len(unapproved_TLD)!= 0):
                is_approved = Website_Filter.is_total_Whitelist_Match(file_WhiteList, unapproved_TLD)
                #If link does not match with any items in whitelist return false
                return is_approved
            return True

WF = Website_Filter()
print(WF.has_SafeMsgLinks('Accepted_Links.txt','apple dsfjisdalkdf www.youtube.com'))
