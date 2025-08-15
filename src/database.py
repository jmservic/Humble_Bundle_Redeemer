import sqlite3
import json
from datetime import datetime

DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

class Database():

    def __init__(self, con_str):
        self._con = sqlite3.connect(con_str)

    def Initialize(self):
        cur = self._con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS HumbleStoreKey(
        HumbleKey NOT NULL, Name NOT NULL, OrderMachineName NOT NULL, Created NOT NULL,
        ProductMachineName NOT NULL, Subproducts, RedeemKey, KeyType, KeyIndex,
        PlatformId, ExpirationDate, Registered NOT NULL,
        CONSTRAINT PK PRIMARY KEY (HumbleKey, ProductMachineName)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS HumbleBundle(
        HumbleKey PRIMARY KEY, Name NOT NULL, OrderMachineName NOT NULL, Created NOT NULL, Subproducts
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS HumbleChoice(
        HumbleKey PRIMARY KEY, Name NOT NULL, OrderMachineName NOT NULL, Created NOT NULL, Subproducts,
        ChoicesRemaining, AllChoices
                     )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Redeemable(
        HumbleKey NOT NULL, Name NOT NULL, ProductMachineName NOT NULL,
        FirstAttempt, LastAttempt, Attempts NOT NULL, Redeemed NOT NULL,
        CONSTRAINT PK PRIMARY KEY (HumbleKey, ProductMachineName),
        FOREIGN KEY (HumbleKey, ProductMachineName) REFERENCES HumbleStoreKey(HumbleKey, ProductMachineName)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Log(
        HumbleKey NOT NULL, Time NOT NULL, Name NOT NULL, ProductMachineName NOT NULL, Action NOT NULL, Success NOT NULL
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Giftable(
        HumbleKey NOT NULL, Name NOT NULL, ProductMachineName NOT NULL, 
        RedeemKey, KeyType, ExpirationDate,
        CONSTRAINT PK PRIMARY KEY (HumbleKey, ProductMachineName),
        FOREIGN KEY (HumbleKey, ProductMachineName) REFERENCES HumbleStoreKey(HumbleKey, ProductMachineName)
                    )""")

    def SaveHumbleLibrary(self, humble_library):
        store_keys_dict = humble_library.GetStoreKeys()
        self.__SaveStoreKeys(store_keys_dict.values())

        bundles_dict = humble_library.GetHumbleBundles()
        self.__SaveBundles("HumbleBundle", bundles_dict.values())
        
        choice_bundles_dict = humble_library.GetChoiceBundles()
        self.__SaveBundles("HumbleChoice", choice_bundles_dict.values())
        self._con.commit()

    def SaveRedeemAttempt(self, humblekey, name, product_machine_name, attempt_time, redeemed):
        date_str = attempt_time.strftime(DT_FORMAT)
        if not self._con.execute("SELECT HumbleKey FROM Redeemable WHERE HumbleKey = ? and ProductMachineName = ?",
                                 (humblekey, product_machine_name)).fetchone():
            row = (humblekey, name, product_machine_name, date_str, date_str, 1, redeemed)
            self._con.execute("INSERT INTO Redeemable VALUES(?, ?, ?, ?, ?, ?, ?)", row) 
            self._con.commit()
        else:
            self._con.execute("""UPDATE Redeemable
                              SET LastAttempt = ?, Attempts = Attempts + 1, Redeemed = ?
                              WHERE HumbleKey = ? and ProductMachineName = ?"""
                              , (date_str, redeemed, humblekey, product_machine_name)) 
            self._con.commit()

    def SaveGift(self, storekey):
        if not self._con.execute("SELECT HumbleKey FROM Giftable WHERE HumbleKey = ? and ProductMachineName = ?",
                                 (storekey.Key(), storekey.ProductMachineName())).fetchone():
            row = (storekey.Key(), storekey.Name(), storekey.ProductMachineName(), storekey.RedeemKey(),
                   storekey.KeyType(), storekey.ExpirationDate())
            self._con.execute("INSERT INTO Giftable VALUES(?, ?, ?, ?, ?, ?)", row)
            self._con.commit()


    def Log(self, humblekey, name, product_machine_name, action, success):
        date_str = datetime.now().strftime(DT_FORMAT)
        row = (humblekey, date_str, name, product_machine_name, action, success)
        self._con.execute("INSERT INTO Log VALUES(?, ?, ?, ?, ?, ?)", row)
        self._con.commit()

    def GetOrders(self):
        orders_dict = {}

        res = self._con.execute("""SELECT HumbleKey, Name, OrderMachineName, Created, Subproducts, ChoicesRemaining,
                                AllChoices FROM HumbleChoice""")
        humble_choices = res.fetchall()

        for choice_row in humble_choices:
            if choice_row[0] not in orders_dict:
                orders_dict[choice_row[0]] = {"HumbleBundle": None,
                                              "HumbleChoice": choice_row,
                                              "StoreKeys": []}

        res = self._con.execute("SELECT HumbleKey, Name, OrderMachineName, Created, Subproducts FROM HumbleBundle")

        humble_bundles = res.fetchall()

        for bundle_row in humble_bundles:
            if bundle_row[0] not in orders_dict:
                orders_dict[bundle_row[0]] = {"HumbleBundle": bundle_row,
                                              "HumbleChoice": None,
                                              "StoreKeys": []}

        res = self._con.execute("""SELECT HumbleKey, Name, OrderMachineName, Created,
        ProductMachineName, Subproducts, RedeemKey, KeyType, KeyIndex,
        PlatformId, ExpirationDate, Registered FROM HumbleStoreKey""")

        storekeys = res.fetchall()

        for storekey_row in storekeys:
            if storekey_row[0] not in orders_dict:
                orders_dict[storekey_row[0]] = {"HumbleBundle": None,
                                                "HumbleChoice": None,
                                                "StoreKeys": [storekey_row]}
            else:
                orders_dict[storekey_row[0]]["StoreKeys"].append(storekey_row)

        return orders_dict


        

    def __SaveStoreKeys(self, store_keys):
        data_inserts = []
        data_updates = []
        for storekey in store_keys:
            if not self._con.execute("SELECT HumbleKey FROM HumbleStoreKey WHERE HumbleKey = ? AND ProductMachineName = ?",
                                     (storekey.Key(), storekey.ProductMachineName())).fetchone():
                expiration_date = storekey.ExpirationDate()
                expiration_str = storekey.ExpirationDate().strftime(DT_FORMAT) if expiration_date else expiration_date
                row = (storekey.Key(), storekey.Name(), storekey.MachineName(), storekey.Created().strftime(DT_FORMAT),
                       storekey.ProductMachineName(), json.dumps(storekey.Subproducts()), storekey.RedeemKey(), storekey.KeyType(),
                       storekey.KeyIndex(), storekey.PlatformId(), expiration_str, storekey.Registered())
                data_inserts.append(row)
            elif storekey.Updated():
                expiration_date = storekey.ExpirationDate()
                expiration_str = storekey.ExpirationDate().strftime(DT_FORMAT) if expiration_date else expiration_date
                row = (storekey.RedeemKey(), storekey.KeyType(), storekey.KeyIndex(), storekey.PlatformId(),
                       expiration_str, storekey.Registered(), storekey.Key(), storekey.ProductMachineName())
                data_updates.append(row)

        if data_inserts:
            self._con.executemany("INSERT INTO HumbleStoreKey VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_inserts)

        if data_updates:
            self._con.executemany("""UPDATE HumbleStoreKey
                                  SET RedeemKey = ?, KeyType = ?, KeyIndex = ?, PlatformId = ?, ExpirationDate = ?, Registered = ?
                                  WHERE HumbleKey = ? AND ProductMachineName = ?""", data_updates)
        

    def __SaveBundles(self, table, bundles):
        for bundle in bundles:
            if not self._con.execute(f"SELECT HumbleKey FROM {table} WHERE HumbleKey = ?", (bundle.Key(),)).fetchone():
                self.__InsertBundle(table, bundle)
            elif bundle.Updated():
                self.__UpdateBundle(table, bundle)
            self.__SaveStoreKeys(bundle.Products())
            
    def __InsertBundle(self, table, bundle):
        match table:
            case "HumbleBundle":
                row = (bundle.Key(), bundle.Name(), bundle.MachineName(), 
                       bundle.Created().strftime(DT_FORMAT), json.dumps(bundle.Subproducts()))
                self._con.execute("INSERT INTO HumbleBundle VALUES(?, ?, ?, ?, ?)", row)
            case "HumbleChoice":
                row = (bundle.Key(), bundle.Name(), bundle.MachineName(), 
                       bundle.Created().strftime(DT_FORMAT), json.dumps(bundle.Subproducts()),
                       bundle.ChoicesRemaining(), json.dumps(bundle.AllChoices()))
                self._con.execute("INSERT INTO HumbleChoice VALUES(?, ?, ?, ?, ?, ?, ?)", row)

    def __UpdateBundle(self, table, bundle):
        match table:
            case "HumbleBundle":
                return
            case "HumbleChoice":
                row = (bundle.ChoicesRemaining(), json.dumps(bundle.AllChoices()), bundle.Key())
                self._con.execute("""UPDATE HumbleChoice
                                  SET ChoicesRemaining = ?, AllChoices = ?
                                  WHERE HumbleKey = ?""", row)

    def close(self):
        if self._con:
            self._con.close()
            self._con = None

    def __del__(self):
        self.close()
