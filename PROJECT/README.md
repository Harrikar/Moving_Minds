# FLL Challenge 2022 - Cargo Connect

Το πρωτότυπό μας αποτελείται από δύο βασικά μέρη, το drone και το airship. 

## Drone Chassis
Για το Drone κατασκευάσαμε τον δικό μας σκελετό με βέργες από αλουμίνιο. Αρχικά είχαμε κατασκευάσει έναν σκελετό σχήματος Η, με λύπη όμως διαπιστώσαμε στις δοκιμές ότι δεν ήταν καθόλου σταθερός. Για να μην επιβαρύνουμε με υπερβολικό βάρος την κατασκευή, χρησιμοποιήσαμε τελικά πιο συμπαγείς ράβδους, όμως μικρότερου μεγέθους, σε σχήμα Χ. Το αποτέλεσμα μας δικαίωσε εν μέρη...

## Flight Controller
Κατασκευάσαμε τον δικό μας Flight Controller, με μικροελεγκτή το Arduino Nano και την ανοιχτή πλατφόρμα [MultiWii](http://www.multiwii.com/). Ευτυχώς υπάρχει πλούσιο υλικό στο internet με οδηγίες και καταφέραμε [να το θέσουμε σε λειτουργία](https://github.com/Harrikar/Moving_Minds/blob/main/Assets/demo_drone.mp4)!

Δεν είναι τόσο σταθερό όσο θα περιμέναμε, όμως είναι ένα drone που κατασκευάσαμε εμείς! Έχουμε βελτιώσει τους συντελεστές PID μέσω της εφαρμογής MultiWii,  χρειάζεται όμως και άλλη προσπάθεια, επειδή η σταθερότητα του drone επηρεάζεται αρκετά όταν προσθέτουμε το υπόλοιπο μέρος της κατασκευής.  

![drone chassis](https://github.com/Harrikar/Moving_Minds/blob/main/Assets/drone%20chassis_2.jpg)

## Σύνθεση
Χρησιμοποιήσαμε επιπλέον το γυροσκόπιο/επιτχυνσιόμετρο GY-521 (MPU6050) και έναν FlυSky Receiver, για να ελέγχουμε απομακρυσμένα το Drone. Επίσης, στο κέντρο τοποθετήσαμε μία πλακέτα για την τροφοδοσία των κινητήρων και του flight controller από την μπαταρία.

![drone on hand](https://github.com/Harrikar/Moving_Minds/blob/main/Assets/drone%20on%20hand_2.jpg)

Για να ενώσουμε το drone με το μπαλόνι, σχεδιάσαμε στο Tinkercad και εκτυπώσαμε σε 3D Printer έναν απλό συνδετικό σκελετό.

![3d printed connector](https://github.com/Harrikar/Moving_Minds/blob/main/Assets/drone%203d%20printed_2.jpg)


