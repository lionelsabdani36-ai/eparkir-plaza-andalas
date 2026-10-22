#!/usr/bin/env python3
"""
Generator for draw.io diagram files (.drawio XML)
Covers E-Parkir Plaza Andalas:
1. flowchart-eparkir.drawio (Parkir Masuk & Parkir Keluar + Kasir)
2. dfd-eparkir.drawio (DFD Level 0 Context & DFD Level 1 Detailed)
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import html

def create_drawio_xml(diagrams):
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'modified': '2026-10-22T04:55:00.000Z',
        'agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        'version': '24.7.17',
        'type': 'device'
    })
    
    for d_name, cells in diagrams.items():
        diagram = ET.SubElement(mxfile, 'diagram', {
            'id': d_name.lower().replace(' ', '-'),
            'name': d_name
        })
        model = ET.SubElement(diagram, 'mxGraphModel', {
            'dx': '1422',
            'dy': '900',
            'grid': '1',
            'gridSize': '10',
            'guides': '1',
            'tooltips': '1',
            'connect': '1',
            'arrows': '1',
            'fold': '1',
            'page': '1',
            'pageScale': '1',
            'pageWidth': '1600',
            'pageHeight': '1400',
            'background': '#060913',
            'math': '0',
            'shadow': '0'
        })
        root = ET.SubElement(model, 'root')
        ET.SubElement(root, 'mxCell', {'id': '0'})
        ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
        
        for c in cells:
            cell_elem = ET.SubElement(root, 'mxCell', c['attrs'])
            if 'geometry' in c:
                ET.SubElement(cell_elem, 'mxGeometry', c['geometry'])
                
    xml_str = ET.tostring(mxfile, encoding='utf-8')
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent='  ')

# =====================================================================
# 1. BUILD FLOWCHART (Parkir Masuk & Parkir Keluar)
# =====================================================================
def build_flowchart():
    cells = []
    
    def add_node(cid, val, style, x, y, w, h):
        cells.append({
            'attrs': {
                'id': cid,
                'value': val,
                'style': style,
                'parent': '1',
                'vertex': '1'
            },
            'geometry': {'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'as': 'geometry'}
        })
        
    def add_edge(eid, src, tgt, val='', style=''):
        default_style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38bdf8;strokeWidth=2;fontColor=#ffffff;labelBackgroundColor=#0a1120;fontSize=11;'
        cells.append({
            'attrs': {
                'id': eid,
                'value': val,
                'style': style or default_style,
                'parent': '1',
                'source': src,
                'target': tgt,
                'edge': '1'
            },
            'geometry': {'relative': '1', 'as': 'geometry'}
        })

    # Styles
    s_start = 'rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#0f172a;strokeColor=#10b981;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=12;'
    s_end   = 'rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#0f172a;strokeColor=#f43f5e;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=12;'
    s_proc  = 'rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#0d172a;strokeColor=#00d2ff;strokeWidth=1.5;fontColor=#ffffff;fontSize=11;spacing=6;'
    s_dec   = 'rhombus;whiteSpace=wrap;html=1;fillColor=#1e1b4b;strokeColor=#f59e0b;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=11;'
    s_io    = 'shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#0f172a;strokeColor=#a855f7;strokeWidth=1.5;fontColor=#ffffff;fontSize=11;'
    s_group = 'swimlane;whiteSpace=wrap;html=1;fillColor=#0a1120;strokeColor=#334155;strokeWidth=1.5;fontColor=#38bdf8;fontStyle=1;fontSize=14;startSize=36;'
    s_warn  = 'rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#450a0a;strokeColor=#f43f5e;strokeWidth=1.5;fontColor=#fecdd3;fontSize=11;spacing=6;'

    # SECTION 1: FLOWCHART PARKIR MASUK
    add_node('grp_in', 'SISTEM PARKIR MASUK (GATE ENTRY)', s_group, 50, 40, 680, 880)
    add_node('in_start', 'Mulai: Kendaraan Tiba<br>di Pintu Masuk', s_start, 290, 90, 200, 50)
    add_node('in_dec_member', 'Apakah Pengguna<br>Member?', s_dec, 310, 180, 160, 90)
    
    # Non-Member Lane (Left)
    add_node('in_nm_print', 'Tekan Tombol &quot;PRINT&quot;<br>di Landing Page Gate', s_io, 100, 310, 190, 60)
    add_node('in_nm_gen', 'Sistem Generate Token Unik<br>&amp; Dynamic QR Code', s_proc, 100, 410, 190, 60)
    add_node('in_nm_db', 'Simpan Waktu Masuk ke DB<br><i>parking_transactions</i>', s_proc, 100, 510, 190, 60)
    add_node('in_nm_struk', 'Cetak Karcis Parkir<br>(Alamat, Token, QR, Tarif)', s_io, 100, 610, 190, 60)

    # Member Lane (Right)
    add_node('in_m_scan', 'Scan QR pada<br>Kartu Member', s_io, 490, 310, 190, 60)
    add_node('in_m_val', 'Sistem Validasi Kode Member<br>&amp; Cek Status Aktif di DB', s_proc, 490, 430, 190, 60)
    add_node('in_m_db', 'Catat Log Waktu Masuk<br>Member ke Database', s_proc, 490, 550, 190, 60)

    # Convergence
    add_node('in_gate_open', 'Palang Pintu Terbuka<br>(Kendaraan Masuk Area)', s_proc, 290, 740, 200, 60)
    add_node('in_end', 'Selesai: Parkir Aktif', s_end, 310, 840, 160, 50)

    # Edges Section 1
    add_edge('e_in_1', 'in_start', 'in_dec_member')
    add_edge('e_in_2', 'in_dec_member', 'in_nm_print', 'Tidak (Non-Member)')
    add_edge('e_in_3', 'in_dec_member', 'in_m_scan', 'Ya (Member)')
    add_edge('e_in_4', 'in_nm_print', 'in_nm_gen')
    add_edge('e_in_5', 'in_nm_gen', 'in_nm_db')
    add_edge('e_in_6', 'in_nm_db', 'in_nm_struk')
    add_edge('e_in_7', 'in_nm_struk', 'in_gate_open')
    add_edge('e_in_8', 'in_m_scan', 'in_m_val')
    add_edge('e_in_9', 'in_m_val', 'in_m_db')
    add_edge('e_in_10', 'in_m_db', 'in_gate_open')
    add_edge('e_in_11', 'in_gate_open', 'in_end')

    # SECTION 2: FLOWCHART PARKIR KELUAR & PEMBAYARAN KASIR
    add_node('grp_out', 'SISTEM PARKIR KELUAR &amp; PEMBAYARAN KASIR', s_group, 780, 40, 780, 1260)
    add_node('out_start', 'Mulai: Kendaraan Tiba di Gate Keluar<br>&amp; Petugas Login ke Sistem', s_start, 1050, 90, 240, 55)
    add_node('out_dec_type', 'Tipe Transaksi<br>di Pintu Keluar?', s_dec, 1070, 185, 200, 95)

    # Non-Member Exit Lane
    add_node('out_nm_scan', 'Petugas Scan QR Karcis /<br>Input Nomor Token', s_io, 820, 320, 220, 60)
    add_node('out_nm_calc_dur', 'Sistem Hitung Durasi Parkir:<br>Durasi = ceil(Keluar - Masuk)', s_proc, 820, 420, 220, 60)
    add_node('out_nm_calc_tag', 'Hitung Tagihan: Tarif Dasar (3rb)<br>+ (Durasi - 1) * Tarif Per Jam', s_proc, 820, 520, 220, 60)
    add_node('out_nm_input_plat', 'Petugas Input Kategori Kendaraan<br>&amp; No. Plat Kendaraan', s_io, 820, 620, 220, 60)

    # Member Exit Lane
    add_node('out_m_menu', 'Buka Menu Member /<br>Scan QR Kartu Member', s_io, 1300, 320, 220, 60)
    add_node('out_m_dec_status', 'Status Pembayaran<br>Bulan Ini?', s_dec, 1310, 420, 200, 85)
    add_node('out_m_lunas_pass', 'Status: LUNAS<br>Palang Terbuka Bebas Biaya', s_proc, 1420, 550, 130, 60)
    add_node('out_m_form_pay', 'Status: BELUM LUNAS<br>Buka Form Payment Member<br>(Tagihan Bulanan Rp 150.000)', s_io, 1230, 550, 180, 70)

    # Shared Payment Process
    add_node('out_cash_in', 'Petugas Input Nominal<br>Uang Tunai dari Pembeli', s_io, 1060, 730, 220, 60)
    add_node('out_calc_change', 'Sistem Hitung Kembalian:<br>Kembalian = Uang Tunai - Tagihan', s_proc, 1060, 830, 220, 60)
    add_node('out_dec_cash', 'Apakah Uang Tunai &gt;=<br>Total Tagihan?', s_dec, 1070, 930, 200, 90)
    add_node('out_err_cash', 'Peringatan: Uang Tunai Kurang!<br>(Tombol Bayar Dinonaktifkan)', s_warn, 820, 945, 200, 60)

    # Finalization
    add_node('out_save_db', 'Simpan Transaksi ke Database<br>&amp; Update Status Member (Lunas)', s_proc, 1060, 1070, 220, 60)
    add_node('out_invoice', 'Tampilkan Notifikasi Sukses,<br>Cetak Invoice &amp; Buka Palang', s_io, 1060, 1160, 220, 60)
    add_node('out_end', 'Selesai: Transaksi Terekam<br>di Laporan Petugas &amp; Admin', s_end, 1080, 1250, 180, 45)

    # Edges Section 2
    add_edge('e_out_1', 'out_start', 'out_dec_type')
    add_edge('e_out_2', 'out_dec_type', 'out_nm_scan', 'Non-Member')
    add_edge('e_out_3', 'out_dec_type', 'out_m_menu', 'Member')
    add_edge('e_out_4', 'out_nm_scan', 'out_nm_calc_dur')
    add_edge('e_out_5', 'out_nm_calc_dur', 'out_nm_calc_tag')
    add_edge('e_out_6', 'out_nm_calc_tag', 'out_nm_input_plat')
    add_edge('e_out_7', 'out_nm_input_plat', 'out_cash_in')
    
    add_edge('e_out_8', 'out_m_menu', 'out_m_dec_status')
    add_edge('e_out_9', 'out_m_dec_status', 'out_m_lunas_pass', 'Lunas')
    add_edge('e_out_10', 'out_m_dec_status', 'out_m_form_pay', 'Belum Lunas')
    add_edge('e_out_11', 'out_m_form_pay', 'out_cash_in')
    add_edge('e_out_12', 'out_m_lunas_pass', 'out_end', 'Selesai Bebas Biaya')

    add_edge('e_out_13', 'out_cash_in', 'out_calc_change')
    add_edge('e_out_14', 'out_calc_change', 'out_dec_cash')
    add_edge('e_out_15', 'out_dec_cash', 'out_err_cash', 'Tidak')
    add_edge('e_out_16', 'out_err_cash', 'out_cash_in', 'Input Ulang')
    add_edge('e_out_17', 'out_dec_cash', 'out_save_db', 'Ya (Valid)')
    add_edge('e_out_18', 'out_save_db', 'out_invoice')
    add_edge('e_out_19', 'out_invoice', 'out_end')

    return cells

# =====================================================================
# 2. BUILD DFD (Data Flow Diagram Level 0 & Level 1)
# =====================================================================
def build_dfd_level0():
    cells = []
    def add_node(cid, val, style, x, y, w, h):
        cells.append({
            'attrs': {'id': cid, 'value': val, 'style': style, 'parent': '1', 'vertex': '1'},
            'geometry': {'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'as': 'geometry'}
        })
    def add_edge(eid, src, tgt, val='', style=''):
        default_style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38bdf8;strokeWidth=1.5;fontColor=#ffffff;labelBackgroundColor=#0a1120;fontSize=10;'
        cells.append({
            'attrs': {'id': eid, 'value': val, 'style': style or default_style, 'parent': '1', 'source': src, 'target': tgt, 'edge': '1'},
            'geometry': {'relative': '1', 'as': 'geometry'}
        })

    s_entity = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#0f172a;strokeColor=#00d2ff;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=13;'
    s_proc0  = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#1e1b4b;strokeColor=#00d2ff;strokeWidth=3;fontColor=#ffffff;fontStyle=1;fontSize=14;'

    # Context Diagram Elements
    add_node('p0', '0.0<br><br><b>SISTEM INFORMASI E-PARKIR</b><br>(PLAZA ANDALAS)', s_proc0, 600, 320, 240, 240)
    add_node('ent_user', 'ENTITAS EKSTERNAL:<br><b>USER / PELANGGAN</b><br>(Member &amp; Non-Member)', s_entity, 120, 370, 220, 140)
    add_node('ent_petugas', 'ENTITAS EKSTERNAL:<br><b>PETUGAS KASIR</b><br>(Pintu Keluar)', s_entity, 610, 720, 220, 130)
    add_node('ent_admin', 'ENTITAS EKSTERNAL:<br><b>SUPER ADMIN</b><br>(Administrator Tunggal)', s_entity, 1100, 370, 220, 140)

    # Edges: User <-> System
    add_edge('e_u1', 'ent_user', 'p0', '1. Permintaan Print Karcis Token<br>2. Scan QR Kartu Member Gate<br>3. Pembayaran Uang Tunai Parkir')
    add_edge('e_u2', 'p0', 'ent_user', '1. Karcis QR Code &amp; Token Parkir<br>2. Struk Invoice Pembayaran<br>3. Kartu Member Fisik/Digital')

    # Edges: Petugas <-> System
    add_edge('e_p1', 'ent_petugas', 'p0', '1. Data Login &amp; Reset Password<br>2. Scan Token/QR Karcis Keluar<br>3. Input No. Plat, Kategori &amp; Uang Tunai<br>4. Data Registrasi Member (CRUD)')
    add_edge('e_p2', 'p0', 'ent_petugas', '1. Status Sesi Login<br>2. Detail Durasi &amp; Total Tagihan Parkir<br>3. Info Kembalian &amp; Cetak Invoice<br>4. Laporan Transaksi Shift Petugas')

    # Edges: Admin <-> System
    add_edge('e_a1', 'ent_admin', 'p0', '1. Kredensial Login Super Admin<br>2. Manajemen Akun Petugas (CRUD)<br>3. Filter Pencarian Laporan Transaksi')
    add_edge('e_a2', 'p0', 'ent_admin', '1. Info Akun &amp; Hak Akses Petugas<br>2. Rekapitulasi Laporan Transaksi Lengkap<br>(Seluruh Petugas, Member &amp; Non-Member)')

    return cells

def build_dfd_level1():
    cells = []
    def add_node(cid, val, style, x, y, w, h):
        cells.append({
            'attrs': {'id': cid, 'value': val, 'style': style, 'parent': '1', 'vertex': '1'},
            'geometry': {'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'as': 'geometry'}
        })
    def add_edge(eid, src, tgt, val='', style=''):
        default_style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38bdf8;strokeWidth=1.5;fontColor=#ffffff;labelBackgroundColor=#0a1120;fontSize=10;'
        cells.append({
            'attrs': {'id': eid, 'value': val, 'style': style or default_style, 'parent': '1', 'source': src, 'target': tgt, 'edge': '1'},
            'geometry': {'relative': '1', 'as': 'geometry'}
        })

    s_entity = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#0f172a;strokeColor=#00d2ff;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=12;'
    s_proc   = 'rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#1e1b4b;strokeColor=#00d2ff;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=12;'
    s_store  = 'shape=partialRectangle;top=0;bottom=0;fillColor=#0f172a;strokeColor=#a855f7;strokeWidth=2;fontColor=#ffffff;fontStyle=1;fontSize=11;spacingLeft=10;'

    # Entities
    add_node('e_user', 'USER<br>(Pelanggan)', s_entity, 60, 360, 150, 80)
    add_node('e_petugas', 'PETUGAS KASIR<br>(Pintu Keluar)', s_entity, 720, 840, 180, 80)
    add_node('e_admin', 'SUPER ADMIN<br>(Administrator)', s_entity, 1380, 360, 160, 80)

    # 5 Processes
    add_node('p1', '1.0<br>Autentikasi &amp;<br>Reset Password', s_proc, 720, 60, 180, 80)
    add_node('p2', '2.0<br>Manajemen Akun<br>&amp; Data Member', s_proc, 1080, 220, 190, 80)
    add_node('p3', '3.0<br>Registrasi Parkir<br>Masuk (In-Gate)', s_proc, 360, 220, 190, 80)
    add_node('p4', '4.0<br>Transaksi Pembayaran<br>&amp; Cetak Invoice', s_proc, 360, 520, 200, 90)
    add_node('p5', '5.0<br>Pelaporan Keuangan<br>&amp; Transaksi Terpusat', s_proc, 1080, 520, 200, 90)

    # 4 Data Stores
    add_node('d1', 'D1 | users<br>(Akun Petugas &amp; Admin)', s_store, 730, 220, 160, 60)
    add_node('d2', 'D2 | members<br>(Data Pelanggan Berlangganan)', s_store, 720, 380, 180, 60)
    add_node('d3', 'D3 | parking_transactions<br>(Transaksi Masuk/Keluar Non-Member)', s_store, 350, 380, 220, 60)
    add_node('d4', 'D4 | member_payments<br>(Riwayat Pembayaran Bulanan Member)', s_store, 710, 540, 200, 60)

    # Process 1.0 Connections
    add_edge('e_p1_in1', 'e_admin', 'p1', 'Username &amp; Password Admin')
    add_edge('e_p1_in2', 'e_petugas', 'p1', 'Username &amp; Password Petugas')
    add_edge('e_p1_db', 'p1', 'd1', 'Verifikasi Bcrypt Hash')
    add_edge('e_p1_out', 'p1', 'e_petugas', 'Sesi Otorisasi')

    # Process 2.0 Connections
    add_edge('e_p2_adm', 'e_admin', 'p2', 'CRUD Akun Petugas')
    add_edge('e_p2_pet', 'e_petugas', 'p2', 'CRUD Data Member')
    add_edge('e_p2_d1', 'p2', 'd1', 'Simpan Akun Petugas')
    add_edge('e_p2_d2', 'p2', 'd2', 'Simpan Data Member')
    add_edge('e_p2_card', 'p2', 'e_user', 'Kartu Member QR')

    # Process 3.0 Connections (Gate Masuk)
    add_edge('e_p3_u', 'e_user', 'p3', 'Klik Print / Scan Kartu')
    add_edge('e_p3_d3', 'p3', 'd3', 'Simpan Token, QR &amp; Waktu Masuk')
    add_edge('e_p3_d2', 'd2', 'p3', 'Validasi Member Code')
    add_edge('e_p3_out', 'p3', 'e_user', 'Karcis QR Token')

    # Process 4.0 Connections (Pembayaran)
    add_edge('e_p4_pet', 'e_petugas', 'p4', 'Input Token/Plat &amp; Uang Tunai')
    add_edge('e_p4_d3_in', 'd3', 'p4', 'Data Waktu Masuk')
    add_edge('e_p4_d3_up', 'p4', 'd3', 'Update Waktu Keluar, Durasi, Total &amp; Status Selesai')
    add_edge('e_p4_d4', 'p4', 'd4', 'Simpan Pembayaran Bulanan Member')
    add_edge('e_p4_inv', 'p4', 'e_user', 'Invoice Pembayaran Lunas')

    # Process 5.0 Connections (Laporan)
    add_edge('e_p5_d3', 'd3', 'p5', 'Data Transaksi Non-Member')
    add_edge('e_p5_d4', 'd4', 'p5', 'Data Pembayaran Member')
    add_edge('e_p5_d1', 'd1', 'p5', 'Data Petugas Bertugas')
    add_edge('e_p5_adm', 'p5', 'e_admin', 'Rekap Laporan Seluruh Petugas')
    add_edge('e_p5_pet', 'p5', 'e_petugas', 'Laporan Kasir Petugas')

    return cells

if __name__ == '__main__':
    # 1. Flowchart
    fc_cells = build_flowchart()
    fc_xml = create_drawio_xml({'Flowchart E-Parkir Plaza Andalas': fc_cells})
    
    with open('/home/lionelsabdani36/duckvaulta/drawio/flowchart-eparkir.drawio', 'w') as f:
        f.write(fc_xml)
    with open('/var/www/duckvaulta/drawio/flowchart-eparkir.drawio', 'w') as f:
        f.write(fc_xml)
    print('[+] Flowchart draw.io generated successfully.')

    # 2. DFD Level 0 & Level 1 (Multi-page draw.io)
    dfd_l0_cells = build_dfd_level0()
    dfd_l1_cells = build_dfd_level1()
    dfd_xml = create_drawio_xml({
        'DFD Level 0 (Context Diagram)': dfd_l0_cells,
        'DFD Level 1 (Detailed Processes)': dfd_l1_cells
    })
    
    with open('/home/lionelsabdani36/duckvaulta/drawio/dfd-eparkir.drawio', 'w') as f:
        f.write(dfd_xml)
    with open('/var/www/duckvaulta/drawio/dfd-eparkir.drawio', 'w') as f:
        f.write(dfd_xml)
    print('[+] DFD Level 0 & 1 draw.io generated successfully.')
