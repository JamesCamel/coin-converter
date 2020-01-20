# Exchange Rate Chat bot

A Facebook messenger bot based on a finite state machine to convert foreign currency and show diagram of instant rate of exchange.


## Setup

### Prerequisite
* Python 3
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install -r requirements.txt
```

* pygraphviz (For visualizing Finite State Machine)
* [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)

#### Secret Data

`VERIFY_TOKEN` and `ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

**`ngrok` would be used in the following instruction**

```sh
./ngrok http 5000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

## Finite State Machine
![](https://i.imgur.com/Seg5s02.png)

## Usage
### Function1: Convert foreign currency
![](https://scontent.ftpe11-1.fna.fbcdn.net/v/t1.15752-9/48428293_281702979198615_159497042215829504_n.png?_nc_cat=110&_nc_ht=scontent.ftpe11-1.fna&oh=843f5bc1e2f4444c466deafb2324671f&oe=5C952DD4)
### Function2: Show diagram of instant rate of exchange 
![](https://scontent.ftpe11-2.fna.fbcdn.net/v/t1.15752-9/48393343_211402003126976_7262956144698589184_n.png?_nc_cat=108&_nc_ht=scontent.ftpe11-2.fna&oh=c4e7532928834943b539d53661100df6&oe=5C9415E8)



