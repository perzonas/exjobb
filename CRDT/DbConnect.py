import sqlite3
from typing import List, Any


def add(vehicleid):
    newdb = sqlite3.connect(vehicleid)
    c = newdb.cursor()

    c.execute('''CREATE TABLE android_metadata (locale TEXT)''')

    c.execute('''CREATE TABLE customers(_ID integer primary key autoincrement,
                    c_name text not null unique,
                    c_name_id text not null,
                    c_contact text not null,
                    c_phone text not null,
                    c_date integer default 0,
                    c_misc text not null
                )''')

    # c.execute('''CREATE TABLE sqlite_sequence(name,seq)''')

    c.execute('''CREATE TABLE materials(
                    _ID integer primary key autoincrement,
                    m_name text not null unique,
                    m_date integer default 0,
                    m_name_id text not null
                )''')

    c.execute('''CREATE TABLE targets(
                    _ID integer primary key autoincrement,
                    t_parent_id integer default 0,
                    t_name text unique,
                    t_capacity integer not null,
                    t_date integer default 0,
                    t_misc text not null
                )''')

    c.execute('''CREATE TABLE work_orders(
                    _ID integer primary key autoincrement,
                    wo_name text unique,
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

    c.close()


def existdbcheck(dbid):

    try:
        c = sqlite3.connect('file:{}?mode=rw'.format(dbid), uri=True)
        c.close()
        return True
    except sqlite3.OperationalError:
        return False



def dbquery():  # get all of mydb
    conn = sqlite3.connect('WorkOrderData6.db')
    c = conn.cursor()
    c.execute('SELECT * FROM targets')
    r = c.fetchall()
    c.execute('SELECT * from loads')
    r = r + c.fetchall()
    conn.close()
    return r


def dbqueryid(id):  # Query a certain database
    conn = sqlite3.connect('WorkOrderData6.db')
    c = conn.cursor()
    c.execute('SELECT * FROM states WHERE h_target=?', id)  # table names cannot be parametrized
    print(c.fetchone())

    conn.close()

