import sqlite3
import os

table_names = ["graveyard", "customers", "targets", "materials", "waybills", "work_orders", "heaps", "table_properties", "loads", "loads_waybills"]


def addnewdb(myid, dbid):
    try:
        os.mkdir("databases/" + str(myid), 0o777)
        os.chmod("databases/" + str(myid), 0o777)
    except OSError:
        pass

    conn = sqlite3.connect("databases/" + myid + "/" + str(dbid), isolation_level=None)
    os.chmod("databases/" + myid + "/" + str(dbid), 0o777)
    c = conn.cursor()

    # c.execute('''CREATE TABLE android_metadata (locale TEXT)''')

    c.execute('''CREATE TABLE graveyard(_ID integer primary key autoincrement,
                            c_databaseid text not null,
                            c_tablename text not null,
                            c_rowid integer not null
                        )''')

    c.execute('''CREATE TABLE customers(_ID integer primary key autoincrement,
                    c_name text not null,
                    c_name_id text not null,
                    c_contact text not null,
                    c_phone text not null,
                    c_date integer default 0,
                    c_misc text not null
                )''')

    # c.execute('''CREATE TABLE sqlite_sequence(name,seq)''')

    c.execute('''CREATE TABLE materials(
                    _ID integer primary key autoincrement,
                    m_name text not null,
                    m_date integer default 0,
                    m_name_id text not null
                )''')

    c.execute('''CREATE TABLE targets(
                    _ID integer primary key autoincrement,
                    t_parent_id integer default 0,
                    t_name text,
                    t_capacity integer not null,
                    t_date integer default 0,
                    t_misc text not null
                )''')

    c.execute('''CREATE TABLE work_orders(
                    _ID integer primary key autoincrement,
                    wo_name text,
                    wo_customer_id integer,
                    wo_capacity integer default 0,
                    wo_misc text not null,
                    wo_due_time integer default 0,
                    wo_date integer default 0,
                    wo_finished integer default 0,
                    wo_weighing integer default 0,
                    FOREIGN KEY (wo_customer_id) REFERENCES customers (_ID) ON DELETE SET NULL
                )''')

    c.execute('''CREATE TABLE table_properties(
                    _ID integer primary key autoincrement,
                    p_active_material_id integer,
                    p_active_heap_type integer default 0,
                    p_trip_heap_id integer,
                    p_project_heap_id integer,
                    p_cloud_heap_id integer,
                    FOREIGN KEY (p_active_material_id) REFERENCES materials (_ID) ON DELETE SET NULL,
                    FOREIGN KEY (p_trip_heap_id) REFERENCES heaps (_ID) ON DELETE SET NULL,
                    FOREIGN KEY (p_project_heap_id) REFERENCES heaps (_ID) ON DELETE SET NULL,
                    FOREIGN KEY (p_cloud_heap_id) REFERENCES heaps (_ID) ON DELETE SET NULL
                )''')

    c.execute('''CREATE TABLE heaps(
                    _ID integer primary key autoincrement,
                    h_workorder integer,
                    h_target integer,
                    h_date integer default 0,
                    h_finished integer default 0,
                    h_weighing integer default 0,
                    FOREIGN KEY (h_workorder) REFERENCES work_orders (_ID) ON DELETE SET NULL,
                    FOREIGN KEY (h_target) REFERENCES targets (_ID) ON DELETE SET NULL
                )''')

    c.execute('''CREATE TABLE loads(
                    _ID integer primary key autoincrement,
                    l_weight integer,
                    l_date integer,
                    l_fuel integer default 0,
                    l_distance integer default 0,
                    l_tool integer default 0,
                    l_heap integer, l_material integer,
                    FOREIGN KEY (l_heap) REFERENCES heaps (_ID) ON DELETE SET NULL,
                    FOREIGN KEY (l_material) REFERENCES materials (_ID) ON DELETE SET NULL
                )''')

    c.execute('''CREATE TABLE waybills(
                    _ID integer primary key autoincrement,
                    wb_date integer default 0,
                    wb_supplier text not null,
                    wb_customer text not null,
                    wb_workorder text not null,
                    wb_target text not null,
                    wb_freetext text not null,
                    wb_location text not null,
                    wb_operator text not null,wb_obw integer default 0
                )''')

    c.execute('''CREATE TABLE loads_waybills(
                    _ID integer primary key autoincrement,
                    lwb_load integer,
                    lwb_waybill integer,
                    FOREIGN KEY (lwb_load) REFERENCES loads (_ID) ON DELETE CASCADE,
                    FOREIGN KEY (lwb_waybill) REFERENCES waybills (_ID) ON DELETE CASCADE
                )''')

    # c.execute('''CREATE TABLE garbage(
    #                _ID integer primary key autoincrement,
    #                table text not null,
    #                row integer not null
    #            )''')

    c.execute('''CREATE INDEX h_workorder_index ON heaps (h_workorder)''')

    c.execute('''CREATE INDEX h_target_index ON heaps (h_target)''')

    c.execute('''CREATE INDEX h_date_index ON heaps (h_date)''')

    c.execute('''CREATE INDEX l_material_index ON loads (l_material)''')

    c.execute('''CREATE INDEX l_heap_index ON loads (l_heap)''')

    c.execute('''CREATE INDEX l_date_index ON loads (l_date)''')

    c.execute('''CREATE INDEX wo_customer_index ON work_orders (wo_customer_id)''')

    c.execute('''CREATE INDEX wo_finished_index ON work_orders (wo_finished)''')

    c.execute('''CREATE INDEX wo_date_index ON work_orders (wo_date)''')

    c.execute('''CREATE TRIGGER delete_compartments 
                    AFTER DELETE ON targets
                    FOR EACH ROW BEGIN DELETE FROM targets 
                    WHERE t_parent_id = OLD._id; END''')

    c.execute('''CREATE TRIGGER create_compartment_heap BEFORE INSERT ON heaps 
                    WHEN NEW.h_target > 0 AND 
                    (SELECT targets.t_parent_id FROM targets WHERE targets._ID = NEW.h_target LIMIT 1) <= 0 
                    BEGIN INSERT INTO heaps (h_workorder, h_target, h_date, h_finished, h_weighing) 
                    SELECT new. h_workorder, targets, ID, new.h_date, new.h_finished, new.h_weighing FROM targets 
                    WHERE new.h_target = targets.t_parent_id; END''')

    conn.close()


def dbaddentry(myid, dbid, table, entry):
    conn = sqlite3.connect("databases/" + str(myid) + "/" + str(dbid), isolation_level=None)
    c = conn.cursor()
    c.execute("PRAGMA table_info(%s)" % table)
    columns = len(c.fetchall())
    cur = c.execute("SELECT * from %s" % table)
    names = list(map(lambda x: x[0], cur.description))
    cnames = table + "(" + ",".join(names[1:]) + ")"
    try:
        c.execute('''INSERT INTO {tn} VALUES ({q})'''.format(tn=cnames, q=",".join(["?"]*(columns-1))), entry[1:])
    except sqlite3.IntegrityError as e:
        print("row already added: ", e, " ", entry, " ", dbid)

    conn.close()


def dbquery(myid, dbid):  # get all of mydb
    dbaste = {}

    conn = sqlite3.connect("databases/" + str(myid) + "/" + str(dbid))
    c = conn.cursor()

    for name in table_names:
        c.execute("SELECT * FROM %s" % name)
        dbaste[name] = c.fetchall()

    conn.close()
    return dbaste




def dbdeltaquery(myid, dbid, table, nrtograb):
    conn = sqlite3.connect("databases/" + str(myid) + "/" + str(dbid))
    c = conn.cursor()

    c.execute("SELECT * FROM %s ORDER BY _ID DESC LIMIT %s" % (table, str(nrtograb+1)))
    delta_state = c.fetchall()
    delta_state.reverse()
    #final_delta_state = [entry for entry in delta_state if not dbgraveyardcheck(myid, dbid, table, entry[0])]

    conn.close()
    return delta_state


def dbgetsnapshot(myid, dbid):
    state_dict = {}

    conn = sqlite3.connect("databases/" + str(myid) + "/" + str(dbid), isolation_level=None)
    c = conn.cursor()
    seq = c.execute("SELECT * FROM SQLITE_SEQUENCE").fetchall()

    for table in table_names:
        state_dict[table] = 0

    for table, entry in seq:
        state_dict[table] = entry

    conn.close()
    return state_dict


def dbexistcheck(myid, dbid):
    try:
        c = sqlite3.connect("file:{}?mode=rw".format("databases/" + str(myid) + "/" + str(dbid)), uri=True)
        c.close()
        return True
    except sqlite3.OperationalError:
        return False


def dbentryexist(myid, dbid, table, key):
    conn = sqlite3.connect("databases/" + str(myid) + "/" + str(dbid))
    c = conn.cursor()

    r = c.execute("SELECT COUNT(*) FROM %s WHERE _ID = %s" % (table, key)).fetchall()
    conn.close()
    return r[0][0]


def dbgraveyardcheck(myid, dbid, table, key):
    conn = sqlite3.connect("databases/" + str(myid) + "/" + str(dbid))
    c = conn.cursor()

    r = c.execute("SELECT COUNT(*) FROM graveyard WHERE c_databaseid='%s' AND c_tablename = '%s' AND c_rowid = '%s'" % (dbid, table, key)).fetchall()
    conn.close()
    return r[0][0]


def dbdeleteentry(myid, dbid, table, key):
    if not dbgraveyardcheck(myid, dbid, table, key):
        dbaddentry(myid, dbid, "graveyard", (0, dbid, table, key))
