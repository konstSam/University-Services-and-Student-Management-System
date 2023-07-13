import mysql.connector
import random
from tkinter import *


def connect():  # Συνδεση με mysql
    try:
        conn = mysql.connector.connect(
            host="hostname", user="username", passwd="passwd", database="project_database")
    except mysql.connector.Error as e:
        print(e)
        return False
    return conn


# Εμφανίστε τα στοιχεια ολων των φοιτητων ενος συγκεκριμενου ετους εισαγωγης και Μ.Ο.
def students(conn, mycurs):
    try:
        etos = int(input("ΔΩΣΕ ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ: "))
        mycurs.execute(
            "SELECT e.`AM`,s.`name`, s.`etos eisagogis`,AVG(e.`grade`) AS Average, COUNT(e.`AM`) AS `#of Lessons Passed`\
            FROM STUDENT s JOIN EGGRAFI e ON e.`AM`=s.`AM`\
            WHERE e.`grade`>=5 AND s.`etos eisagogis`={} \
            GROUP BY e.`AM` ORDER BY Average DESC, `#of Lessons Passed` DESC;".format(etos))
        alles = mycurs.fetchall()
        print("ΦΟΙΤΗΤΕΣ: \n")
        for x in alles:
            print(
                "ΑΜ: {}, Ονομα: '{}', Ετος Εισαγωγης: {}, Μ.Ο: {}, #of Lessons Passed: {} ".format(*x))

    except mysql.connector.Error as e:
        print(e)


def professor(conn, mycurs):  # Εμφανίστε τα στοιχεια ολων των καθηγητων.
    try:
        mycurs.execute("SELECT * FROM `PROFESSOR`")
        print("ΚΑΘΗΓΗΤΕΣ: \n")
        for x in mycurs:
            print(x)

    except mysql.connector.Error as e:
        print(e)


# Εμφανίστε τα μαθηματα στη βάση δεδομένων κατά αλφαβητικη σειρά.
def lesson(conn, mycurs):
    try:
        mycurs.execute("SELECT `title` FROM `LESSON` ORDER BY `title` ASC")
        print("ΜΑΘΗΜΑΤΑ: \n")
        for x in mycurs:
            print(x[0])

    except mysql.connector.Error as e:
        print(e)


# Εμφανιζει τα μαθηματα που ειναι κορμου ή κατευθυνσης και σε ποιαν κατευθ ανηκει
def lesson_kormou_tomea(conn, mycurs):
    ans = int(
        input("Θες να δεις τα μαθηματα του Κορμου (1) ή της Κατευθυνσης (2) ? (1/2): "))
    try:
        if ans == 1:
            mycurs.execute("SELECT l.`lesson id`,l.`title`,d.`semester` \
                FROM kormou k JOIN LESSON l ON l.`lesson id`=k.`id_mathima`\
                JOIN DIDASKALIA d ON l.`lesson id`=d.`kod math`\
                ORDER BY d.`semester`;")
            print("ΜΑΘΗΜΑΤΑ: \n")
            for x in mycurs:
                print("ID: {}, ΤΙΤΛΟΣ: '{}', ΕΞΑΜΗΝΟ: {} ".format(*x))
        elif ans == 2:
            mycurs.execute("SELECT l.`lesson id`,l.`title`,d.`semester`,k.`onoma tomea` \
                FROM tomea t JOIN LESSON l ON l.`lesson id`=t.`id_mathima` \
                JOIN KATEYTHINSI k ON k.`t_id`=t.`omada`\
                JOIN DIDASKALIA d ON l.`lesson id`=d.`kod math`\
                ORDER BY d.`semester`;")
            print("ΜΑΘΗΜΑΤΑ: \n")
            for x in mycurs:
                print("ID: {}, ΤΙΤΛΟΣ: '{}', ΕΞΑΜΗΝΟ: {} , ΚΑΤΕΥΘΥΝΣΗ: '{}' ".format(*x))
        else:
            print("Λαθος αριθμος")

    except mysql.connector.Error as e:
        print(e)


def lesson_erg(conn, mycurs):  # Εμφανιζει τα μαθηματα που εχουν εργαστηριο
    try:
        mycurs.execute("SELECT l.`lesson id`,l.`title`,d.`semester` \
            FROM `LESSON` l JOIN DIDASKALIA d ON l.`lesson id`=d.`kod math`\
            WHERE d.`ergastirio`='YES' ORDER BY d.`semester`;")
        print("ΤΑ ΜΑΘΗΜΑΤΑ ΠΟΥ ΕΧΟΥΝ ΕΡΓΑΣΤΗΡΙΟ ΕΙΝΑΙ ΤΑ: \n")
        for x in mycurs:
            print("ID: {}, ΤΙΤΛΟΣ: '{}', ΕΞΑΜΗΝΟ: {} ".format(*x))

    except mysql.connector.Error as e:
        print(e)


# Εμφανίστε τα μαθηματα, τα ects, αν ειναι υποχρεωτικα, το εξαμηνο στο οποιο διδασκονται κατα σειρα εξαμηνου και τον καθηγητη.
def didaskalia(conn, mycurs):
    try:
        mycurs.execute("SELECT l.`title`,d.`semester`,l.`ECTS`, p.`name` AS professor \
            FROM DIDASKALIA d JOIN LESSON l ON d.`kod math`=l.`lesson id` \
            JOIN DIDASKEI did ON d.`kod math`=did.`lesson`\
            JOIN PROFESSOR p ON p.`AM`=did.`AM prof`\
            ORDER BY d.`semester` ASC;")
        print("ΔΙΔΑΣΚΑΛΙΑ: \n")
        for x in mycurs:
            print(
                "title: {},  semester: {},  ECTS: {},  professor: {}".format(*x))

    except mysql.connector.Error as e:
        print(e)


# Εμφανιστε τους φοιτητες (ΑΜ,ονομα) που ειναι εγγεγραμμενοι σε ενα συγκεκριμενο μαθημα, το βαθμο τους και το εξαμηνο.
def eggegrammenoi_ana_mathima(conn, mycurs):
    lesson(conn, mycurs)
    m = input("Δωσε μαθημα: ")
    try:
        mycurs.execute("SELECT s.`AM`,s.`name`,e.`semester`,e.`grade`\
            FROM eggrafi e JOIN student s ON e.`AM`=s.`AM`\
            JOIN didaskalia d ON d.`kod math`=e.`id math`\
            JOIN lesson l ON d.`kod math`=l.`lesson id`\
            WHERE l.`title`= %s;", (m,))
        print("Εγγεγραμμενοι στο μαθημα : '{}'".format(m))
        for x in mycurs:
            print("ΑΜ: {}, ΟΝΟΜΑ: '{}', ΕΞΑΜΗΝΟ: {}, ΒΑΘΜΟΣ: {}".format(*x))

    except mysql.connector.Error as e:
        print(e)


def ptyxiouxoi(conn, mycurs):  # Βρισκει τους φοιτητες που μπορουν να παρουν πτυχιο
    try:
        mycurs.execute("SELECT COUNT(*) FROM LESSON;")
        math = mycurs.fetchone()[0]
        mycurs.execute("SELECT e.`AM`,s.`name`,s.`etos eisagogis`, AVG(e.`grade`) AS `Average Grade` \
            FROM EGGRAFI e JOIN STUDENT s ON e.`AM`=s.`AM` \
            WHERE e.`grade`>=5  \
            GROUP BY e.`AM` \
            HAVING COUNT(e.`AM`)>={} \
            ORDER BY `Average Grade` DESC;".format(int(math)))
        print("Μπορουν να παρουν ή εχουν πτυχιο: ")
        for x in mycurs:
            print("AM: {},  ΟΝΟΜΑ: '{}',  ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ: {},  Μ.Ο: {}".format(*x))

    except mysql.connector.Error as e:
        print(e)


def kateythinseis(conn, mycurs):  # Εμφανιζει ολες τις κατευθυνσεις
    try:
        mycurs.execute("SELECT * FROM KATEYTHINSI;")
        print("\nΥπαρχουν οι εξης κατευθυνσεις: ")
        for x in mycurs:
            print("ID: {}, ΟΝΟΜΑ: '{}'".format(*x))

    except mysql.connector.Error as e:
        print(e)


def subs_kateythinsi(conn, mycurs):  # Δηλωση κατευθυνσης απο φοιτητη
    am = int(input("ΔΩΣΕ ΤΟ ΑΜ ΣΟΥ: "))
    kateythinseis(conn, mycurs)
    ans = int(input("ΕΠΙΛΕΞΕ ΤΟ ID ΤΗΣ ΚΑΤΕΥΘΥΝΣΗΣ ΠΟΥ ΘΕΣ ΝΑ ΚΑΝΕΙΣ ΕΓΓΡΑΦΗ: "))
    try:
        mycurs.execute(
            "UPDATE STUDENT SET `kid`= {} WHERE `AM`={}".format(ans, am))
        conn.commit()
        print('Επιτυχης επιλογή κατευθυνσης.')

    except mysql.connector.Error as e:
        print(e)


# Λιστα με ολους τους φοιτητες μιας κατευθυνσης που επιλεγει ο χρηστης
def students_kateythinseis(conn, mycurs):
    try:
        kateythinseis(conn, mycurs)
        kat = input("ΔΩΣΕ ΚΑΤΕΥΘΥΝΣΗ: ")
        mycurs.execute("SELECT s.`AM`,s.`name` FROM KATEYTHINSI k \
        JOIN STUDENT s ON k.`t_id`=s.`kid` WHERE k.`onoma tomea`= '{}';".format(kat))
        print("Στην κατευθυνση {} υπαρχουν οι εξης φοιτητες: ".format(kat))
        for x in mycurs:
            print("AM: {}, ΟΝΟΜΑ: '{}'".format(*x))

    except mysql.connector.Error as e:
        print(e)


# Βρισκει AM φοιτ,ονομα φοιτητη,καθηγητη και τιτλο διπλωματικης
def diplwmatikes(conn, mycurs):
    try:
        mycurs.execute("SELECT s.`AM`,s.`name`,p.`name` AS professor,d.`title` \
            FROM DIPLOMATIKI d JOIN STUDENT s ON d.`AM STUDENT`=s.`AM`\
            JOIN PROFESSOR p ON d.`epiblepon`= p.`AM`;")
        print("Διπλωματικες: \n")
        for x in mycurs:
            print("ΑΜ: {}, Φοιτητης: '{}', Καθηγητης: '{}', Τιτλος: '{}'".format(*x))

    except mysql.connector.Error as e:
        print(e)


def add_diplomatikh(conn, mycurs):  # ΕΙΣΑΓΩΓΗ ΝΕΑΣ ΔΙΠΛΩΜΑΤΙΚΗΣ
    mycurs.execute('SELECT COUNT(*) FROM `DIPLOMATIKI`;')

    diplid = mycurs.fetchone()[0]+1
    amStudent = input('ΔΩΣΕ ΑΜ ΦΟΙΤΗΤΗ:')
    amEpiblepontos = input('ΔΩΣΕ ΑΜ ΕΠΙΒΛΕΠΟΝΤΟΣ:')
    title = input('ΔΩΣΕ ΤΟΝ ΤΙΤΛΟ ΤΗΣ ΔΙΠΛΩΜΑΤΙΚΗΣ:')

    try:
        mycurs.execute('INSERT INTO `DIPLOMATIKI` VALUES({},"{}","{}","{}",CURRENT_DATE,CURRENT_DATE + INTERVAL 1 YEAR);'.format(
            diplid, amStudent, amEpiblepontos, title))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)


def update_diplomatikh(conn, mycurs):  # Ανανεωση στοιχειων διπλωματικης
    am = int(input('ΔΩΣΕ ΑΜ ΦΟΙΤΗΤΗ: '))
    mycurs.execute(
        "SELECT * FROM DIPLOMATIKI WHERE `AM student`= {}".format(am))
    print("AM ΕΠΙΒΛΕΠΟΝΤΟΣ (1), ΤΙΤΛΟΣ (2)")
    for x in mycurs:
        print(x)
    num = int(input("Πατα τον αριθμο που αντιπροσωπευει τι θελεις να ανανεωσεις: "))
    if num == 1:
        inp = int(input("Δωσε τα νεα στοιχεια: "))
        mycurs.execute(
            "UPDATE DIPLOMATIKI SET `epiblepon` = {} WHERE `AM student` = {}".format(inp, am))
        conn.commit()
        mycurs.execute(
            "UPDATE DIPLOMATIKI SET `assignment date` = CURRENT_DATE WHERE `AM student` = {}".format(am))
        conn.commit()
        mycurs.execute(
            "UPDATE DIPLOMATIKI SET `min completion date` = CURRENT_DATE + INTERVAL 1 YEAR WHERE `AM student` = {}".format(am))
        conn.commit()
    elif num == 2:
        inp = input("Δωσε τα νεα στοιχεια: ")
        mycurs.execute(
            "UPDATE DIPLOMATIKI SET `title` = '{}' WHERE `AM student` = {}".format(inp, am))
        conn.commit()
        mycurs.execute(
            "UPDATE DIPLOMATIKI SET `assignment date` = CURRENT_DATE WHERE `AM student` = {}".format(am))
        conn.commit()
        mycurs.execute(
            "UPDATE DIPLOMATIKI SET `min completion date` = CURRENT_DATE + INTERVAL 1 YEAR WHERE `AM student` = {}".format(am))
        conn.commit()
    print("Eπιτυχης Καταχωρηση")


def add_student(conn, mycurs):  # ΕΙΣΑΓΩΓΗ ΝΕΟΥ ΦΟΙΤΗΤΗ
    mycurs.execute('SELECT COUNT(*) FROM `STUDENT`;')
    am = mycurs.fetchone()[0]+1
    onoma = input('ΔΩΣΕ ΟΝΟΜΑ ΦΟΙΤΗΤΗ:')
    birthdate = input('ΔΩΣΕ ΗΜΕΡΟΜΗΝΙΑ ΓΕΝΝΗΣΗΣ (YYYY-MM-DD):')
    etos_eisagogis = int(input('ΔΩΣΕ ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ:'))
    email = input('ΔΩΣΕ EMAIL:')
    mothername = input('ΔΩΣΕ ΟΝΟΜΑ ΜΗΤΕΡΑΣ ΦΟΙΤΗΤΗ:')
    fathername = input('ΔΩΣΕ ΟΝΟΜΑ ΠΑΤΕΡΑ ΦΟΙΤΗΤΗ:')
    address = input('ΔΩΣΕ ΤΗΝ ΟΔΟ ΤΟΥ ΦΟΙΤΗΤΗ:')
    status = input('ΕΙΝΑΙ ΠΡΟΠΤΥΧΙΑΚΟΣ Ή ΜΕΤΑΠΤΥΧΙΑΚΟΣ (GRAD/POST-GRAD):')
    phone = input('ΔΩΣΕ ΤΗΛΕΦΩΝΟ ΦΟΙΤΗΤΗ:')
    try:
        mycurs.execute('INSERT INTO `STUDENT` VALUES({},"{}","{}",{},"{}","{}","{}","{}","{}","YES","{}",NULL);'.format(
            am, onoma, birthdate, etos_eisagogis, email, mothername, fathername, address, status, phone))
        conn.commit()
        print("Eπιτυχης Καταχωρηση")

    except mysql.connector.Error as e:
        print(e)


def update_student(conn, mycurs):  # Ανανεωση στοιχειων φοιτητη
    am = int(input('ΔΩΣΕ ΑΜ ΦΟΙΤΗΤΗ: '))
    mycurs.execute("SELECT * FROM STUDENT WHERE `AM`= {}".format(am))
    print("AM (1), name (2), birthdate (3), etos eisagogis (4), email (5), mothername (6), fathername (7), address (8), status (9), active student (10), phone (11), id Κατευθυνσης (12)")
    for x in mycurs:
        print(x)
    num = int(input("Πατα τον αριθμο που αντιπροσωπευει τι θελεις να ανανεωσεις: "))
    if num == 1:
        inp = int(input("Δωσε τα νεα στοιχεια: "))
        mycurs.execute(
            "UPDATE STUDENT SET `AM` = {} WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 2:
        inp = input("Δωσε τα νεα στοιχεια: ")
        mycurs.execute(
            "UPDATE STUDENT SET `name` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 3:
        inp = input("Δωσε τα νεα στοιχεια (Μορφη YYYY-MM-DD): ")
        mycurs.execute(
            "UPDATE STUDENT SET `birthdate` = {} WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 4:
        inp = int(input("Δωσε τα νεα στοιχεια: "))
        mycurs.execute(
            "UPDATE STUDENT SET `etos eisagogis` = {} WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 5:
        inp = input("Δωσε τα νεα στοιχεια: ")
        mycurs.execute(
            "UPDATE STUDENT SET `email` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 6:
        inp = input("Δωσε τα νεα στοιχεια: ")
        mycurs.execute(
            "UPDATE STUDENT SET `mothername` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 7:
        inp = input("Δωσε τα νεα στοιχεια: ")
        mycurs.execute(
            "UPDATE STUDENT SET `fathername` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 8:
        inp = input("Δωσε τα νεα στοιχεια: ")
        mycurs.execute(
            "UPDATE STUDENT SET `address` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 9:
        inp = input("Δωσε τα νεα στοιχεια (GRAD/POST-GRAD): ")
        mycurs.execute(
            "UPDATE STUDENT SET `status` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 10:
        inp = input("Δωσε τα νεα στοιχεια (Yes/No): ")
        mycurs.execute(
            "UPDATE STUDENT SET `active student` = '{}' WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 11:
        inp = int(input("Δωσε τα νεα στοιχεια: "))
        mycurs.execute(
            "UPDATE STUDENT SET `phone` = {} WHERE `AM` = {}".format(inp, am))
        conn.commit()
    elif num == 12:
        inp = int(input("Δωσε τα νεα στοιχεια: "))
        mycurs.execute(
            "UPDATE STUDENT SET `kid` = {} WHERE `AM` = {}".format(inp, am))
        conn.commit()
    print("Eπιτυχης Καταχωρηση")


def add_professor(conn, mycurs):  # ΕΙΣΑΓΩΓΗ ΝΕΟΥ ΚΑΘΗΓΗΤΗ
    mycurs.execute('SELECT COUNT(*) FROM `PROFESSOR`;')
    am = mycurs.fetchone()[0]+1
    onoma = input('ΔΩΣΕ ΟΝΟΜΑ ΚΑΘΗΓΗΤΗ:')
    address = input('ΔΩΣΕ ΤΗΝ ΟΔΟ ΤΟΥ ΚΑΘΗΓΗΤΗ:')
    email = input('ΔΩΣΕ EMAIL:')
    status = input(
        'ΕΠΙΛΕΞΕ STATUS (Επίκουρος Καθηγητής, Καθηγητής, Αναπληρωτης Καθηγητής):')
    phone = input('ΔΩΣΕ ΤΗΛΕΦΩΝΟ ΚΑΘΗΓΗΤΗ:')
    try:
        mycurs.execute('INSERT INTO `PROFESSOR` VALUES({},"{}","{}","{}","{}",{});'.format(
            am, onoma, address, email, status, phone))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)


def update_professor(conn, mycurs):  # Ανανεωση στοιχειων καθηγητη ή διαγραφη
    ans = int(input(
        "ΘΕΣ ΝΑ ΑΝΑΝΕΩΣΕΙΣ ΤΑ ΣΤΟΙΧΕΙΑ (1) Ή ΝΑ ΔΙΑΓΡΑΨΕΙΣ ΕΝΑΝ ΚΑΘΗΓΗΤΗ (2) ? (1/2): "))
    try:
        if ans == 1:
            am = int(input('ΔΩΣΕ ΑΜ ΚΑΘΗΓΗΤΗ: '))
            mycurs.execute("SELECT * FROM PROFESSOR WHERE `AM`= {}".format(am))
            print("AM (1), name (2), address (3), email (4), status (5), phone (6)")
            for x in mycurs:
                print(x)
            num = int(
                input("Πατα τον αριθμο που αντιπροσωπευει, τι θελεις να ανανεωσεις: "))
            if num == 1:
                inp = int(input("Δωσε τα νεα στοιχεια: "))
                mycurs.execute(
                    "UPDATE PROFESSOR SET `AM` = {} WHERE `AM` = {}".format(inp, am))
                conn.commit()
            elif num == 2:
                inp = input("Δωσε τα νεα στοιχεια: ")
                mycurs.execute(
                    "UPDATE PROFESSOR SET `name` = '{}' WHERE `AM` = {}".format(inp, am))
                conn.commit()
            elif num == 3:
                inp = input("Δωσε τα νεα στοιχεια: ")
                mycurs.execute(
                    "UPDATE PROFESSOR SET `address` = '{}' WHERE `AM` = {}".format(inp, am))
                conn.commit()
            elif num == 4:
                inp = int(input("Δωσε τα νεα στοιχεια: "))
                mycurs.execute(
                    "UPDATE PROFESSOR SET `email` = '{}' WHERE `AM` = {}".format(inp, am))
                conn.commit()
            elif num == 5:
                inp = input(
                    "Δωσε τα νεα στοιχεια (Επίκουρος Καθηγητής, Καθηγητής, Αναπληρωτης Καθηγητής): ")
                mycurs.execute(
                    "UPDATE PROFESSOR SET `status` = '{}' WHERE `AM` = {}".format(inp, am))
                conn.commit()
            elif num == 6:
                inp = input("Δωσε τα νεα στοιχεια: ")
                mycurs.execute(
                    "UPDATE PROFESSOR SET `phone` = {} WHERE `AM` = {}".format(inp, am))
                conn.commit()
            print("Eπιτυχης Καταχωρηση")
        elif ans == 2:
            am = int(input('ΔΩΣΕ ΑΜ ΚΑΘΗΓΗΤΗ: '))
            mycurs.execute('DELETE FROM `PROFESSOR` WHERE `AM`={}'.format(am))
            conn.commit()
            print("Επιτυχης διαγραφη.")
        else:
            print("Λαθος αριθμος.")

    except mysql.connector.Error as e:
        print(e)


def add_didaskalia(conn, mycurs):  # ΕΙΣΑΓΩΓΗ ΔΙΔΑΣΚΑΛΙΑΣ
    idmathim = input('ΔΩΣΕ ΚΩΔΙΚΟ ΜΑΘΗΜΑΤΟΣ:')
    idmathim = int(idmathim)
    semester = input('ΔΩΣΕ ΤΟ ΕΞΑΜΗΝΟ :')
    semester = int(semester)
    erg = input("ΕΧΕΙ ΕΡΓΑΣΤΗΡΙΟ ? (YES/NO): ")
    try:
        mycurs.execute('INSERT INTO `DIDASKALIA` VALUES({},{},"{}");'
                       .format(idmathim, semester, erg))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)


def update_didaskalia(conn, mycurs):  # UPDATE / DELETE ΔΙΔΑΣΚΑΛΙΑ
    ans = int(
        input("ΘΕΣ ΝΑ ΑΛΛΑΞΕΙΣ (1) Ή ΝΑ ΔΙΑΓΡΑΨΕΙΣ ΜΙΑ ΔΙΔΑΣΚΑΛΙΑ (2) ? (1/2): "))
    try:
        if ans == 1:
            idmathim = input('ΔΩΣΕ ΚΩΔΙΚΟ ΜΑΘΗΜΑΤΟΣ:')
            idmathim = int(idmathim)
            semester = input('ΔΩΣΕ ΤΟ ΝΕΟ ΕΞΑΜΗΝΟ :')
            semester = int(semester)
            erg = input("ΕΧΕΙ ΕΡΓΑΣΤΗΡΙΟ ? (YES/NO): ")
            mycurs.execute('UPDATE `DIDASKALIA` SET `semester`= {} WHERE `kod math`={}'.format(
                semester, idmathim))
            conn.commit()
            mycurs.execute('UPDATE `DIDASKALIA` SET `ergastirio`= "{}" WHERE `kod math`={}'.format(
                erg, idmathim))
            conn.commit()
            print("Επιτυχης Καταχωρηση.")
        elif ans == 2:
            idmathim = input('ΔΩΣΕ ΚΩΔΙΚΟ ΜΑΘΗΜΑΤΟΣ:')
            idmathim = int(idmathim)
            mycurs.execute(
                'DELETE FROM `DIDASKALIA` WHERE `kod math`={}'.format(idmathim))
            conn.commit()
            print("Επιτυχης Διαγραφη.")
        else:
            print("Λαθος αριθμος.")

    except mysql.connector.Error as e:
        print(e)


def sub(conn, mycurs):  # Δηλωση μαθηματων- Εγγραφη σε διδασκαλια
    am = input("ΔΩΣΕ ΤΟ ΑΜ ΣΟΥ: ")
    sem = input("ΔΩΣΕ ΤΟ ΕΞΑΜΗΝΟ ΣΟΥ: ")
    mycurs.execute(
        "SELECT l.`title`,d.`kod math` FROM DIDASKALIA d JOIN LESSON l ON d.`kod math`=l.`lesson id`")
    lessons = mycurs.fetchall()
    i = 0
    for x in lessons:
        print("'{}', ID: {}".format(*x))
        i += 1
    exodos = 'YES'
    while exodos != 'NO':
        idmat = int(
            input("Σε ποιο μαθημα θες να εγγραφεις? Γραψε το ID του μαθηματος: "))
        try:
            mycurs.execute(
                "INSERT INTO EGGRAFI VALUES ({},{},{},NULL,CURRENT_DATE());".format(am, idmat, sem))
            conn.commit()
            print("Η εγγραφη ηταν επιτυχης!")
            exodos = input("Θες να εγγραφεις και σε αλλο μαθημα? (YES/NO): ")

        except mysql.connector.Error as e:
            print(e)

    print("Τελος εγγραφης.")


def grades(conn, mycurs):  # Περασμα βαθμων απο διαχειριστη
    mycurs.execute("SELECT l.`lesson id`,d.`semester`,l.`title` \
        FROM `LESSON` l JOIN DIDASKALIA d ON l.`lesson id`=d.`kod math`\
        ORDER BY d.`semester`;")
    les = mycurs.fetchall()
    for x in les:
        print("ID: {}, ΕΞΑΜΗΝΟ: {} , Τιτλος: '{}'".format(*x))
    telos = 'YES'
    while telos != 'NO':
        idlesson = int(
            input("ΔΩΣΕ ID ΜΑΘΗΜΑΤΟΣ ΠΟΥ ΘΕΣ ΝΑ ΠΕΡΑΣΕΙΣ ΒΑΘΜΟΛΟΓΙΕΣ: "))
        mycurs.execute(
            "SELECT `id math`,`AM`,`semester` FROM eggrafi WHERE `grade` IS NULL AND `id math`={}".format(idlesson))
        st = mycurs.fetchall()
        for x in st:
            print("ID: {},AM: {}, SEMESTER: {}".format(*x))

        ex = 'YES'
        while ex != 'NO':
            am = int(
                input("Σε ποιον φοιτητη θες να περασεις βαθμο? Γραψε το ΑΜ του ΦΟΙΤΗΤΗ: "))
            sem = int(input("Δωσε το ΕΞΑΜΗΝΟ ΦΟΙΤΗΤΗ: "))
            grad = float(input("Δωσε το ΒΑΘΜΟ του: "))
            try:
                mycurs.execute(
                    "UPDATE EGGRAFI SET `grade`= {} WHERE `id math`={} AND `AM`={} AND `semester`={};".format(grad, idlesson, am, sem))
                conn.commit()
                print("Ο βαθμος περαστικε επιτυχως!")
                ex = input(
                    "Θες να περασεις βαθμο και σε αλλο ΦΟΙΤΗΤΗ? (YES/NO): ")

            except mysql.connector.Error as e:
                print(e)
        telos = input(
            "Θες να περασεις βαθμολογια και για ΑΛΛΟ μαθημα ? (YES/NO): ")
    print("Τελος Βαθμολογησης.")


def add_pistopoihtiko(conn, mycurs):  # Προσθηκη νεου πιστοποιητικου
    mycurs.execute('SELECT COUNT(*) FROM `PISTOPOIHTIKO`;')
    pid = mycurs.fetchone()[0]+1
    typos = input('ΔΩΣΕ ΤΟΝ ΤΥΠΟ ΤΟΥ ΝΕΟΥ ΠΙΣΤΟΠΟΙΗΤΙΚΟΥ: ')
    try:
        mycurs.execute(
            "INSERT INTO PISTOPOIHTIKO VALUES ({},'{}');".format(pid, typos))
        conn.commit()
        print("Η προσθηκη νεου πιστοποιητικου ηταν επιτυχης!")

    except mysql.connector.Error as e:
        print(e)


# Βρισκει ολες τις αιτησεις πιστοποιητικων που δεν εχουν ολοκληρωθει.
def uncompleted_request(conn, mycurs):
    mycurs.execute("SELECT a.`AM`,s.`name`,a.`p_id`,p.`type`,a.`date` FROM AITEITAI a \
        JOIN PISTOPOIHTIKO p ON a.`p_id`=p.`p_id`\
        JOIN STUDENT s ON a.`AM`=s.`AM`\
        WHERE a.`completed`='NO';")
    for x in mycurs:
        print("ΑΜ: {}, ΟΝΟΜΑ: '{}', ID ΠΙΣΤΟΠ: {}, ΤΥΠΟΣ: '{}', ΗΜΕΡΟΜΗΝΙΑ ΑΙΤΗΣΗΣ: '{}' ".format(*x))


def aitisi(conn, mycurs):  # Ο φοιτητης δημιουργει μια αιτηση
    am = int(input("ΔΩΣΕ ΤΟ ΑΜ ΣΟΥ: "))
    mycurs.execute("SELECT * FROM PISTOPOIHTIKO;")
    for x in mycurs:
        print("ID: {}, Τυπος: '{}' ".format(*x))
    inp = int(input("Πατα το id της αιτησης που σε ενδιαφερει: "))
    try:
        mycurs.execute(
            "INSERT INTO AITEITAI VALUES ({},{},CURRENT_DATE(),'NO');".format(am, inp))
        conn.commit()
        print("Η δημιουργια αιτησης πιστοποιητικου ηταν επιτυχης!")

    except mysql.connector.Error as e:
        print(e)


def st_aitiseis(conn, mycurs):  # Ο φοιτητης μπορει να δει ολες τις αιτησεις που εχει κανει
    am = int(input("ΔΩΣΕ ΤΟ ΑΜ ΣΟΥ: "))
    mycurs.execute("SELECT a.`AM`,s.`name`,p.`type`,a.`date`,a.`completed` FROM AITEITAI a \
        JOIN PISTOPOIHTIKO p ON a.`p_id`=p.`p_id`\
        JOIN STUDENT s ON a.`AM`=s.`AM`\
        WHERE a.`AM`= {}".format(am))
    for x in mycurs:
        print("ΑΜ: {}, ΟΝΟΜΑ: '{}', ΤΥΠΟΣ: '{}', ΗΜΕΡΟΜΗΝΙΑ ΑΙΤΗΣΗΣ: '{}',ΟΛΟΚΛΗΡΩΜΕΝΗ: '{}'".format(*x))

# -------------------------------------------------------------------------------------------------------------------------


def all_lessons(conn, mycurs):  # Επιστρεφει το συνολικο αριθμο μαθηματων στη βαση
    try:
        mycurs.execute('SELECT COUNT(*) FROM `LESSON`;')
        rows = mycurs.fetchall()
        number = rows[0]
        return int(number[0])

    except mysql.connector.Error as e:
        print(e)


def didaskei(conn, mycurs):  # Γεμιζουμε τον πινακα ΔΙΔΑΣΚΕΙ
    num_of_lessons = all_lessons(conn, mycurs)
    mycurs.execute('SELECT `am` FROM `PROFESSOR`;')
    kath = []
    for x in mycurs:
        kath.append(x[0])
    len1 = num_of_lessons + 1
    for i in range(1, len1):
        random_didaskei = kath[random.randint(0, len(kath)-1)]
        try:
            mycurs.execute(
                'INSERT INTO `DIDASKEI` VALUES ({},{});'.format(random_didaskei, i))
            conn.commit()

        except mysql.connector.Error as e:
            print(e)
# -----------------------------------------------------------Main-----------------------------------------------------------


def main():

    conn = connect()
    if conn.is_connected():
        print("\nΗ σύνδεση με τη βάση δεδομένων ήταν επιτυχής.")

    # Δημιουργια cursor για τις ερωτησεις-εισαγωγες δεδομενων
    mycurs = conn.cursor()

    while(1):
        print("\nΕπιλογή λειτουργίας:\n1:Φοιτητής\n2:Διαχειριστής\n3:Έξοδος")
        ans = input("Επιλογή:")

        if(ans == "1"):
            print("User mode")
            window = Tk()
            window.title("Υπηρεσίες Φοιτητή: Λειτουργία Φοιτητή")
            w = 800
            h = 400
            window.geometry('%dx%d+%d+%d' % (w, h, 0, 0))

            # READ
            read = Label(window, text="ΠΛΗΡΟΦΟΡΙΕΣ").grid(column=0, row=0)
            # Εμφανίστε τα στοιχεια ολων των καθηγητων.
            profBtn = Button(window, text="Εμφάνιση πληροφοριων των καθηγητών",
                             command=lambda: professor(conn, mycurs)).grid(column=0, row=1)
            # Εμφανίστε τα μαθηματα στη βάση δεδομένων κατά αλφαβητικη σειρά.
            lessons1Btn = Button(window, text="Εμφάνιση όλων των μαθημάτων", command=lambda: lesson(
                conn, mycurs)).grid(column=0, row=2)
            # Εμφανίστε τα μαθηματα κορμου/κατεθυνσης.
            lessons2Btn = Button(window, text="Εμφάνιση μαθηματα κορμου ή κατευθυνσης",
                                 command=lambda: lesson_kormou_tomea(conn, mycurs)).grid(column=0, row=3)
            # Εμφανιζει τα μαθηματα που εχουν εργαστηριο
            lessons3Btn = Button(window, text="Εμφάνιση μαθηματων με εργαστηριο",
                                 command=lambda: lesson_erg(conn, mycurs)).grid(column=0, row=4)
            # Εμφανίστε τις ενεργες διδασκαλιες που πραγματοποιουνται
            lessons4Btn = Button(window, text="Εμφάνιση ενεργων Διδασκαλιων",
                                 command=lambda: didaskalia(conn, mycurs)).grid(column=0, row=5)
            # Λιστα με όλες τις κατευθύνσεις
            kateuBtn = Button(window, text="Εμφάνιση όλων των κατευθύνσεων",
                              command=lambda: kateythinseis(conn, mycurs)).grid(column=0, row=6)
            # Εμφανιση όλων των διπλωματικών
            diplBtn = Button(window, text="Εμφάνιση όλων των διπλωματικών",
                             command=lambda: diplwmatikes(conn, mycurs)).grid(column=0, row=7)
            # Ιστορικό αιτήσεων πιστοποιητικών
            allPistopBtn = Button(window, text="Ιστορικό αιτήσεων πιστοποιητικών",
                                  command=lambda: st_aitiseis(conn, mycurs)).grid(column=0, row=8)

            # CREATE
            create = Label(window, text="ΔΗΛΩΣΕΙΣ").grid(column=1, row=0)
            # Ο φοιτητής εγγράφεται στον μαθημα που επιθυμεί
            addLessonBtn = Button(window, text="Δήλωση Μαθημάτων", command=lambda: sub(
                conn, mycurs)).grid(column=1, row=1)
            # Επιλογή κατευθυνσης
            addKatBtn = Button(window, text="Δήλωση Κατευθυνσης", command=lambda: subs_kateythinsi(
                conn, mycurs)).grid(column=1, row=2)
            # Επιλογή διπλωματικής
            addDiploBtn = Button(window, text="Δήλωση Διπλωματικής", command=lambda: add_diplomatikh(
                conn, mycurs)).grid(column=1, row=3)
            # Αίτηση πιστοποιητικού
            addPistopBtn = Button(window, text="Νέα αίτηση πιστοποιητικού",
                                  command=lambda: aitisi(conn, mycurs)).grid(column=1, row=4)

            # UPDATE
            update = Label(window, text="ΕΝΗΜΕΡΩΣΗ").grid(column=2, row=0)
            # Αλλαγή κατευθυνσης
            updateKatBtn = Button(window, text="Αλλαγή Κατεύθυνσης", command=lambda: subs_kateythinsi(
                conn, mycurs)).grid(column=2, row=1)
            # Αλλαγή διπλωματικής
            updateDiploBtn = Button(window, text="Αλλαγή Διπλωματικής", command=lambda: update_diplomatikh(
                conn, mycurs)).grid(column=2, row=2)

            window.mainloop()
        elif(ans == "2"):
            print("Admin mode")

            password = input("Δώσε κωδικό πρόσβασης διαχειριστή:")
            if(password == "123"):
                window = Tk()
                window.title("Υπηρεσίες Φοιτητή: Λειτουργία Διαχειριστή")
                w = 900
                h = 400
                window.geometry('%dx%d+%d+%d' % (w, h, 0, 0))

                # READ
                read = Label(window, text="ΠΛΗΡΟΦΟΡΙΕΣ").grid(column=0, row=0)
                # Εμφανίστε τα στοιχεια ολων των φοιτητων ενος συγκεκριμενου ετους εισαγωγης.
                studentsBtn = Button(window, text="Εμφάνιση όλων των φοιτητών ενός συγκεκριμένου έτους εισαγωγής",
                                     command=lambda: students(conn, mycurs)).grid(column=0, row=1)
                # Εμφανίστε τα στοιχεια ολων των καθηγητων.
                profBtn = Button(window, text="Εμφάνιση όλων των καθηγητών", command=lambda: professor(
                    conn, mycurs)).grid(column=0, row=2)
                # Εμφανίστε τα μαθηματα στη βάση δεδομένων κατά αλφαβητικη σειρά.
                lessonsBtn = Button(window, text="Εμφάνιση όλων των μαθημάτων", command=lambda: lesson(
                    conn, mycurs)).grid(column=0, row=3)
                # Εμφανίστε τα μαθηματα, τα ects, αν ειναι υποχρεωτικα, το εξαμηνο στο οποιο διδασκονται κατα σειρα εξαμηνου και τον καθηγητη.
                classesBtn = Button(window, text="Εμφάνιση όλων των μαθημάτων που διδάσκονται",
                                    command=lambda: didaskalia(conn, mycurs)).grid(column=0, row=4)
                # Εμφανιστε τους φοιτητες (ΑΜ,ονομα) που ειναι εγγεγραμμενοι σε ενα συγκεκριμενο μαθημα, το βαθμο τους και το εξαμηνο.
                eggegrBtn = Button(window, text="Εμφάνιση όλων των φοιτητών που ειναι εγγεγραμμένοι σε ένα μάθημα",
                                   command=lambda: eggegrammenoi_ana_mathima(conn, mycurs)).grid(column=0, row=5)
                # Βρισκει τους φοιτητες που μπορουν να παρουν πτυχιο
                ptyxBtn = Button(window, text="Εμφάνιση όλων των φοιτητών που μπορούν να πάρουν πτυχίο",
                                 command=lambda: ptyxiouxoi(conn, mycurs)).grid(column=0, row=6)
                # Λιστα με ολους τους φοιτητες μιας κατευθυνσης που επιλεγει ο χρηστης
                kateuBtn = Button(window, text="Εμφάνιση όλων των φοιτητών μίας κατεύθυνσης",
                                  command=lambda: students_kateythinseis(conn, mycurs)).grid(column=0, row=7)
                # Βρισκει AM φοιτ,ονομα φοιτητη,καθηγητη και τιτλο διπλωματικης
                diploBtn = Button(window, text="Εμφάνιση όλων ενεργών διπλωματικών",
                                  command=lambda: diplwmatikes(conn, mycurs)).grid(column=0, row=8)
                # Εμφανιση όλων των πιστοποιητικών προς έγκριση
                pendingBtn = Button(window, text="Εμφανιση όλων των πιστοποιητικών προς έγκριση",
                                    command=lambda: uncompleted_request(conn, mycurs)).grid(column=0, row=9)

                # CREATE
                create = Label(window, text="ΕΙΣΑΓΩΓΗ").grid(column=1, row=0)
                # ΕΙΣΑΓΩΓΗ ΝΕΟΥ ΦΟΙΤΗΤΗ
                addStudentBtn = Button(window, text="Εισαγωγή νέου φοιτητή", command=lambda: add_student(
                    conn, mycurs)).grid(column=1, row=1)
                # ΕΙΣΑΓΩΓΗ ΝΕΟΥ ΚΑΘΗΓΗΤΗ
                addProfessorBtn = Button(window, text="Εισαγωγή νέου καθηγητή", command=lambda: add_professor(
                    conn, mycurs)).grid(column=1, row=2)
                # ΕΙΣΑΓΩΓΗ ΔΙΔΑΣΚΑΛΙΑΣ
                addClassBtn = Button(window, text="Εισαγωγή νέου μαθήματος/διδασκαλίας",
                                     command=lambda: add_didaskalia(conn, mycurs)).grid(column=1, row=3)
                # ΕΙΣΑΓΩΓΗ ΒΑΘΜΩΝ
                addGradesBtn = Button(window, text="Εισαγωγή βαθμών", command=lambda: grades(
                    conn, mycurs)).grid(column=1, row=4)
                # Προσθηκη νεου πιστοποιητικου
                addPistopBtn = Button(window, text="Προσθηκη νεου πιστοποιητικου",
                                      command=lambda: add_pistopoihtiko(conn, mycurs)).grid(column=1, row=5)

                # UPDATE
                update = Label(window, text="ΕΝΗΜΕΡΩΣΗ").grid(column=2, row=0)
                # Ανανεωση στοιχειων φοιτητή
                updateStudentBtn = Button(window, text="Ανανέωση στοιχείων φοιτητή", command=lambda: update_student(
                    conn, mycurs)).grid(column=2, row=1)
                # Ανανεωση στοιχειων καθηγητή
                updateProfessorBtn = Button(window, text="Ανανέωση στοιχείων καθηγητή", command=lambda: update_professor(
                    conn, mycurs)).grid(column=2, row=2)
                # Ανανεωση στοιχειων διδασκαλίας
                updateClassBtn = Button(window, text="Ανανέωση μαθήματος/διδασκαλίας",
                                        command=lambda: update_didaskalia(conn, mycurs)).grid(column=2, row=3)

                window.mainloop()
        elif(ans == "3"):
            break


if __name__ == "__main__":
    main()
