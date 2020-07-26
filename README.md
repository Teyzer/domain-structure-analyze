
# Explorer Web

Explorer-web is a simple app in which a given url will be analyzed and the structure of the targetted website will be returned, including phone number and mails, or more if wanted. The content of each page will be analyzed to find new links, whether pages of the same domain or other domains. 

## Table of contents
* [Technology](#technology)
* [Setup](#setup)
* [Usage](#usage)
* [Example](#example)

## Technology
The project is built with Python `3.8.1` but will basically work with all version of python `3.X.X`
No other language is used.
It use `requests` to get content of pages, so you will obviously need a network connection.

## Setup
Just do the basic steps:
* First download the project with 
`git clone https://github.com/Teyzer/explorer-web`
* Enter folder
`cd explorer-web`
* Install requirements ( use `pip3` instead of `pip` on debian-based devices )
`pip install -r requirements.txt`

## Usage

Launch the app with `python explorer.py -t <target_url>`
You can also use some few other settings, as can be showed with `python explorer.py -h` (help) :
```
Help / Usage  
  -t <target_url> : Specify the starting url ( required )  
  -m <max> : Specify the max number of page to visit ( optional )  
  --explore-all : If you want to explore not same-origin domain as well ( optional )  
                  If used, please specify a maximum too, if not the thread will be infinite  
  --only-domain : If you want to visit only the homepage of each domain ( optional )
```

**(1) Warning :** It is recommanded to use the `-m` argument if you want a quick result. You will get a better result with a high limit ( and a perfect one if you don't set any limit ) but the time will also increase. For example, if you scan https://nordvpn without limit, the app will scan all the page of nordvpn that can be find ( so around 1700 pages ! ) and you sure can easily guess that it will take a much bigger time.
**(2) Warning :** `-m` is not used to specify the max of elements that will be rendered but the number of page that will be scanned in research of new links, phone numbers and mails.

## Example

If I want to render the architecture of https://github.com by scanning its first 5 pages, I would type :
`python explorer.py -t https://github.com -m 5` 
And it would render a thing like this after taking some time to get the content of the 5 first pages:
```
github.com/  
├─── github.com/  
├─── about/  
├─── about/ ─── careers/  
├─── about/ ─── press/  
├─── atom/ ─── atom/  
├─── business/  
├─── collections/  
├─── contact/  
├─── customer-stories/  
├─── customer-stories/ ─── freakboy3742/  
├─── customer-stories/ ─── jessfraz/  
├─── customer-stories/ ─── kris-nova/  
├─── customer-stories/ ─── mgm-resorts/  
├─── customer-stories/ ─── nationwide/  
├─── customer-stories/ ─── sap/  
├─── customer-stories/ ─── spotify/  
├─── customer-stories/ ─── yyx990803/  
├─── electron/ ─── electron/  
├─── enterprise/  
├─── events/  
├─── explore/  
├─── features/  
├─── features/ ─── actions/  
├─── features/ ─── actions/  
├─── features/ ─── code-review/  
├─── features/ ─── code-review/  
├─── features/ ─── integrations/  
├─── features/ ─── integrations/  
├─── features/ ─── package-registry/  
├─── features/ ─── packages/  
├─── features/ ─── project-management/  
├─── features/ ─── project-management/  
├─── features/ ─── security/  
├─── git-guides/  
├─── git-lfs/ ─── git-lfs/  
├─── github/  
├─── github/ ─── hubot/  
├─── join/  
├─── login/  
├─── marketplace/  
├─── marketplace/ ─── codacy/  
├─── marketplace/ ─── codecov/  
├─── marketplace/ ─── codefactor/  
├─── marketplace/ ─── codetree/  
├─── marketplace/ ─── coveralls/  
├─── marketplace/ ─── stale/  
├─── marketplace/ ─── zenhub/  
├─── marketplace/ ─── zube/  
├─── mobile/  
├─── mobile/  
├─── nonprofit/  
├─── open-source/  
├─── organizations/ ─── enterprise_plan/  
├─── personal/  
├─── pricing/  
├─── security/  
├─── site-map/  
├─── site/ ─── privacy/  
├─── site/ ─── terms/  
├─── team/  
├─── topics/  
├─── trending/  
└─── works-with/
```
In the example above, the software did not found any phone number or email, but here's what can be rendered when the software find phone number and/or mails in the website.

```
[+] Found following mails :  
[-] support@nordvpn.com  
[-] social@nordvpnmedia.com  
[-] press@nordvpnmedia.com  
[-] careers@nordvpn.com  
[-] press@nordvpnpr.com  
[-] business@nordvpn.com  
[-] sales@nordvpnbusiness.com
```
