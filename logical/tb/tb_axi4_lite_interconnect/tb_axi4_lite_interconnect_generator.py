import sys
import os
import random


def parse_args(arg):
    if not arg.startswith("m") or "s" not in arg:
        raise ValueError("Format must be 'm{n}s{n}', example: m2s1")
    m_part, s_part = arg[1:].split("s")
    return int(m_part), int(s_part)


def generate_tb(m, s):
    tb = []

    # header
    tb.append(f"`timescale 1ns / 1ns\n")
    tb.append(f"module tb_axi4_lite_interconnect_m{m}s{s}();")

    # address parameters
    tb.append(f"    /* address parameters */")
    for i in range(s):
        start_addr = i * 0x100
        end_addr = start_addr + 0xFF
        tb.append(f"    parameter LOW_ADDR{i}     = 32'h{start_addr:08x};")
        tb.append(f"    parameter HIGH_ADDR{i}    = 32'h{end_addr:08x};")
    tb.append("")

    # clock and reset
    tb.append("    parameter           CLK_PERIOD = 10;")
    tb.append("    reg                 iCLK, iRST;")
    tb.append("")

    # master interfaces
    for master in range(m):
        tb.append(f"    /* master {master} interfaces */")
        tb.append(f"    reg                 m{master}_write_req;")
        tb.append(f"    reg     [3:0]       m{master}_write_strb;")
        tb.append(
            f"    reg     [31:0]      m{master}_write_addr, m{master}_write_data;"
        )
        tb.append(f"    wire    [1:0]       m{master}_write_resp;")
        tb.append(f"    ")
        tb.append(f"    reg                 m{master}_read_req;")
        tb.append(f"    reg     [31:0]      m{master}_read_addr;")
        tb.append(f"    wire    [1:0]       m{master}_read_resp;")
        tb.append(f"    wire    [31:0]      m{master}_read_data;")
        tb.append(f"    ")
        tb.append(f"    ")

    # master signals
    for master in range(m):
        tb.append(f"    /* master {master} signals */")
        tb.append(f"    wire                m{master}_AWVALID, m{master}_AWREADY;")
        tb.append(f"    wire    [31:0]      m{master}_AWADDR;")
        tb.append(f"    ")
        tb.append(f"    wire                m{master}_WVALID, m{master}_WREADY;")
        tb.append(f"    wire    [3:0]       m{master}_WSTRB;")
        tb.append(f"    wire    [31:0]      m{master}_WDATA;")
        tb.append(f"    ")
        tb.append(f"    wire                m{master}_BREADY, m{master}_BVALID;")
        tb.append(f"    wire    [1:0]       m{master}_BRESP;")
        tb.append(f"    ")
        tb.append(f"    wire                m{master}_ARVALID, m{master}_ARREADY;")
        tb.append(f"    wire    [31:0]      m{master}_ARADDR;")
        tb.append(f"    ")
        tb.append(f"    wire                m{master}_RREADY, m{master}_RVALID;")
        tb.append(f"    wire    [1:0]       m{master}_RRESP;")
        tb.append(f"    wire    [31:0]      m{master}_RDATA;")
        tb.append(f"    ")
        tb.append(f"    ")

    # slave signals
    for slave in range(s):
        tb.append(f"    /* slave {slave} signals */")
        tb.append(f"    wire                s{slave}_AWVALID, s{slave}_AWREADY;")
        tb.append(f"    wire    [31:0]      s{slave}_AWADDR;")
        tb.append(f"    ")
        tb.append(f"    wire                s{slave}_WVALID, s{slave}_WREADY;")
        tb.append(f"    wire    [3:0]       s{slave}_WSTRB;")
        tb.append(f"    wire    [31:0]      s{slave}_WDATA;")
        tb.append(f"    ")
        tb.append(f"    wire                s{slave}_BREADY, s{slave}_BVALID;")
        tb.append(f"    wire    [1:0]       s{slave}_BRESP;")
        tb.append(f"    ")
        tb.append(f"    wire                s{slave}_ARVALID, s{slave}_ARREADY;")
        tb.append(f"    wire    [31:0]      s{slave}_ARADDR;")
        tb.append(f"    ")
        tb.append(f"    wire                s{slave}_RREADY, s{slave}_RVALID;")
        tb.append(f"    wire    [1:0]       s{slave}_RRESP;")
        tb.append(f"    wire    [31:0]      s{slave}_RDATA;")
        tb.append(f"    ")
        tb.append(f"    ")

    # slave memories
    for slave in range(s):
        tb.append(f"    /* slave {slave} memory */")
        tb.append(
            f"    wire    [1:0]       slave{slave}_write_resp, slave{slave}_read_resp;"
        )
        tb.append(f"    reg     [31:0]      write{slave}_addr, read{slave}_addr;")
        tb.append(f"    reg     [31:0]      slave{slave}_mem [0:255];")
        tb.append(f"    wire                slave{slave}_write_data_done;")
        tb.append(
            f"    wire    [31:0]      slave{slave}_read_data, slave{slave}_write_addr, slave{slave}_write_data, slave{slave}_read_addr;"
        )
        tb.append(
            f"    wire                slave{slave}_write_addr_done, slave{slave}_read_addr_done;"
        )
        tb.append(f"    ")
        tb.append(f"    ")

    # test control variables
    tb.append(f"    integer         i;")
    tb.append(f"    integer         idx, valid_idx, try_idx, found;")
    tb.append(f"    integer         total_ops = 0;")
    tb.append(f"    ")
    tb.append(f"    reg             has_written[0:24];")
    tb.append(f"    reg     [31:0]  addr_list [0:24];")
    tb.append(f"    reg     [31:0]  data_list [0:24];")
    tb.append(f"    ")

    # instantiate masters
    for master in range(m):
        tb.append(f"    axi4_lite_master #(")
        tb.append(f"        .ADDR_WIDTH(32), .DATA_WIDTH(32)")
        tb.append(f"    ) u_master{master} (")
        tb.append(f"        .iCLK(iCLK), .iRST(iRST),")
        tb.append(f"        ")
        tb.append("        /* write */")
        tb.append(
            f"        .m_AWREADY(m{master}_AWREADY), .m_AWVALID(m{master}_AWVALID), .m_AWPROT(), .m_AWADDR(m{master}_AWADDR),"
        )
        tb.append(
            f"        .m_WREADY(m{master}_WREADY), .m_WVALID(m{master}_WVALID), .m_WDATA(m{master}_WDATA), .m_WSTRB(m{master}_WSTRB),"
        )
        tb.append(
            f"        .m_BVALID(m{master}_BVALID), .m_BRESP(m{master}_BRESP), .m_BREADY(m{master}_BREADY),"
        )
        tb.append(f"        ")
        tb.append("        /* read */")
        tb.append(
            f"        .m_ARREADY(m{master}_ARREADY), .m_ARVALID(m{master}_ARVALID), .m_ARPROT(), .m_ARADDR(m{master}_ARADDR),"
        )
        tb.append(
            f"        .m_RVALID(m{master}_RVALID), .m_RRESP(m{master}_RRESP), .m_RDATA(m{master}_RDATA), .m_RREADY(m{master}_RREADY),"
        )
        tb.append(f"        ")
        tb.append("        /* interfaces */")
        tb.append(
            f"        .write_req(m{master}_write_req), .write_addr(m{master}_write_addr), .write_data(m{master}_write_data), .write_strb(m{master}_write_strb), .write_resp(m{master}_write_resp),"
        )
        tb.append(
            f"        .read_req(m{master}_read_req), .read_addr(m{master}_read_addr), .read_data(m{master}_read_data), .read_resp(m{master}_read_resp)"
        )
        tb.append(f"    );")
        tb.append(f"    ")

    # instantiate slaves
    for slave in range(s):
        tb.append(f"    axi4_lite_slave #(")
        tb.append(f"        .ADDR_WIDTH(32), .DATA_WIDTH(32)")
        tb.append(f"    ) u_slave{slave} (")
        tb.append(f"        .iCLK(iCLK), .iRST(iRST),")
        tb.append(f"        ")
        tb.append("        /* write */")
        tb.append(
            f"        .s_AWVALID(s{slave}_AWVALID), .s_AWPROT(3'b0), .s_AWADDR(s{slave}_AWADDR), .s_AWREADY(s{slave}_AWREADY),"
        )
        tb.append(
            f"        .s_WVALID(s{slave}_WVALID), .s_WDATA(s{slave}_WDATA), .s_WSTRB(s{slave}_WSTRB), .s_WREADY(s{slave}_WREADY),"
        )
        tb.append(
            f"        .s_BREADY(s{slave}_BREADY), .s_BVALID(s{slave}_BVALID), .s_BRESP(s{slave}_BRESP),"
        )
        tb.append(f"        ")
        tb.append("        /* read */")
        tb.append(
            f"        .s_ARVALID(s{slave}_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s{slave}_ARADDR), .s_ARREADY(s{slave}_ARREADY),"
        )
        tb.append(
            f"        .s_RREADY(s{slave}_RREADY), .s_RVALID(s{slave}_RVALID), .s_RRESP(s{slave}_RRESP), .s_RDATA(s{slave}_RDATA),"
        )
        tb.append(f"        ")
        tb.append("        /* interfaces */")
        tb.append(
            f"        .write_addr(slave{slave}_write_addr), .write_data(slave{slave}_write_data),.write_strb(slave{slave}_write_strb), .write_resp(slave{slave}_write_resp),"
        )
        tb.append(
            f"        .read_data(slave{slave}_read_data), .read_addr(slave{slave}_read_addr), .read_resp(slave{slave}_read_resp)"
        )
        tb.append(f"    );")
        tb.append(f"    ")

    # instantiate interconnect
    tb.append(f"    axi4_lite_interconnect_m{m}s{s} #(")
    for slave in range(s):
        start_addr = 0x100 + (slave * 0x100)
        end_addr = start_addr + 0x100
        tb.append(
            f"        .LOW_ADDR{slave}(LOW_ADDR{slave}), .HIGH_ADDR{slave}(HIGH_ADDR{slave}){',' if slave != s-1 else ''}"
        )
    tb.append(f"    ) u_interconnect (")
    tb.append(f"        .iCLK(iCLK), .iRST(iRST),")
    tb.append(f"        ")

    # master connections
    for master in range(m):
        tb.append(f"        /* master {master} signals */")
        tb.append(
            f"        .m{master}_AWVALID(m{master}_AWVALID), .m{master}_AWADDR(m{master}_AWADDR), .m{master}_AWREADY(m{master}_AWREADY),"
        )
        tb.append(
            f"        .m{master}_WVALID(m{master}_WVALID), .m{master}_WSTRB(m{master}_WSTRB), .m{master}_WDATA(m{master}_WDATA), .m{master}_WREADY(m{master}_WREADY),"
        )
        tb.append(
            f"        .m{master}_BREADY(m{master}_BREADY), .m{master}_BVALID(m{master}_BVALID), .m{master}_BRESP(m{master}_BRESP),"
        )
        tb.append(
            f"        .m{master}_ARVALID(m{master}_ARVALID), .m{master}_ARADDR(m{master}_ARADDR), .m{master}_ARREADY(m{master}_ARREADY),"
        )
        tb.append(
            f"        .m{master}_RREADY(m{master}_RREADY), .m{master}_RVALID(m{master}_RVALID), .m{master}_RRESP(m{master}_RRESP), .m{master}_RDATA(m{master}_RDATA){',' if master != m-1 or s > 0 else ''}"
        )
        tb.append(f"        ")

    # slave connections
    for slave in range(s):
        tb.append(f"        /* slave {slave} signals */")
        tb.append(
            f"        .s{slave}_AWREADY(s{slave}_AWREADY), .s{slave}_AWVALID(s{slave}_AWVALID), .s{slave}_AWADDR(s{slave}_AWADDR),"
        )
        tb.append(
            f"        .s{slave}_WREADY(s{slave}_WREADY), .s{slave}_WVALID(s{slave}_WVALID), .s{slave}_WSTRB(s{slave}_WSTRB), .s{slave}_WDATA(s{slave}_WDATA),"
        )
        tb.append(
            f"        .s{slave}_BVALID(s{slave}_BVALID), .s{slave}_BRESP(s{slave}_BRESP), .s{slave}_BREADY(s{slave}_BREADY),"
        )
        tb.append(
            f"        .s{slave}_ARREADY(s{slave}_ARREADY), .s{slave}_ARVALID(s{slave}_ARVALID), .s{slave}_ARADDR(s{slave}_ARADDR), "
        )
        tb.append(
            f"        .s{slave}_RVALID(s{slave}_RVALID), .s{slave}_RRESP(s{slave}_RRESP), .s{slave}_RDATA(s{slave}_RDATA), .s{slave}_RREADY(s{slave}_RREADY)"
            + (",\n" if slave != s - 1 else "")
        )

    tb.append(f"    );")
    tb.append(f"    ")

    # slave memory models
    for slave in range(s):
        tb.append(f"    /* slave {slave} memory model */")
        tb.append(f"    always @(posedge iCLK) begin")
        tb.append(
            f"        if (slave{slave}_write_addr_done) write{slave}_addr <= slave{slave}_write_addr;"
        )
        tb.append(
            f"        if (slave{slave}_write_data_done) slave{slave}_mem[write{slave}_addr] <= slave{slave}_write_data;"
        )
        tb.append(
            f"        if (slave{slave}_read_addr_done) read{slave}_addr <= slave{slave}_read_addr;"
        )
        tb.append(f"    end")
        tb.append(f"    ")
        tb.append(
            f"    assign slave{slave}_read_data         = slave{slave}_mem[read{slave}_addr];"
        )
        tb.append(
            f"    assign slave{slave}_write_addr_done   = s{slave}_AWVALID && s{slave}_AWREADY;"
        )
        tb.append(
            f"    assign slave{slave}_write_data_done   = s{slave}_WVALID  && s{slave}_WREADY;"
        )
        tb.append(
            f"    assign slave{slave}_read_addr_done    = s{slave}_ARVALID && s{slave}_ARREADY;"
        )
        tb.append(f"    assign slave{slave}_write_resp        = 2'b00;")
        tb.append(f"    assign slave{slave}_read_resp         = 2'b00;")
        tb.append(f"    ")

    # clock generation
    tb.append(f"    initial begin")
    tb.append(f"        iCLK = 1'b1;")
    tb.append(f"        forever #(CLK_PERIOD/2) iCLK = ~iCLK;")
    tb.append(f"    end")
    tb.append(f"    ")

    # initial reset and control signals
    tb.append(f"    initial begin")
    tb.append(f"        iRST             = 1'b0;")
    for master in range(m):
        tb.append(f"        m{master}_write_req     = 1'b0;")
        tb.append(f"        m{master}_write_strb    = 4'b0;")
        tb.append(f"        m{master}_write_addr    = 32'h0;")
        tb.append(f"        m{master}_write_data    = 32'h0;")
        tb.append(f"        m{master}_read_req      = 1'b0;")
        tb.append(f"        m{master}_read_addr     = 32'h0;")
    tb.append(f"    ")
    tb.append(f"        /* memory initialization */")
    for slave in range(s):
        tb.append(f"        write{slave}_addr      = 32'h0;")
        tb.append(f"        read{slave}_addr       = 32'h0;")
    tb.append(f"    end")
    tb.append(f"    ")

    # generate address and data list
    tb.append(f"    /* generate address and data list */")
    tb.append(f"    initial begin")
    tb.append(f"        for (i = 0; i < 25; i = i + 1) begin")
    tb.append(f"            if ($urandom % 2)")
    tb.append(f"                addr_list[i] = 32'h00000100 + (($urandom % 64) * 4);")
    tb.append(f"            else")
    tb.append(f"                addr_list[i] = 32'h00000000 + (($urandom % 64) * 4);")
    tb.append(f"            ")
    tb.append(f"            data_list[i] = $urandom;")
    tb.append(f"        end")
    tb.append(f"    end")
    tb.append(f"    ")

    # test sequence
    tb.append(f"    /* test case */")
    tb.append(f"    initial begin")
    tb.append(
        f'        $dumpfile("logical/sim/axi4_lite_interconnect/axi4_lite_interconnect_m{m}s{s}.vcd");'
    )
    tb.append(f"        $dumpvars(0, tb_axi4_lite_interconnect_m{m}s{s});")
    tb.append(f"    ")
    tb.append(f"        /* init memory */")
    tb.append(f"        for (i = 0; i < 256; i = i + 1) begin")
    for slave in range(s):
        tb.append(f"            slave{slave}_mem[i] = 32'h0;")
    tb.append(f"        end")
    tb.append(f"    ")
    tb.append(f"        for (i = 0; i < 25; i = i + 1)")
    tb.append(f"            has_written[i] = 1'b0;")
    tb.append(f"    ")
    tb.append(f"        #10; iRST = 1'b1;")
    tb.append(f"    ")
    tb.append(
        f'        $display("\\n[INFO] Memulai simulasi AXI4-Lite Interconnect (random read/write)\\n");'
    )
    tb.append(f"    ")
    tb.append(f"        while (total_ops < 50) begin")
    tb.append(f"            if ($urandom_range(0, 1)) begin")
    tb.append(f"                /* ================== WRITE ================== */")
    tb.append(f"                ")
    tb.append(f"                idx = $urandom_range(0, 24);")
    tb.append(f"    ")
    tb.append(
        f'                $display("[WRITE] Addr = 0x%08h, Data = 0x%08h", addr_list[idx], data_list[idx]);'
    )
    tb.append(f"    ")
    tb.append(f"                m0_write_addr       <= addr_list[idx];")
    tb.append(f"                m0_write_data       <= data_list[idx];")
    tb.append(f"                m0_write_strb       <= 4'b1111;")
    tb.append(f"                m0_write_req        <= 1'b1;")
    tb.append(f"    ")
    tb.append(f"                @(posedge m0_BREADY);")
    tb.append(f"                    m0_write_req    <= 1'b0;")
    tb.append(f"    ")
    tb.append(f"                has_written[idx]    = 1'b1;")
    tb.append(f"    ")
    tb.append(f"            end else begin")
    tb.append(f"                /* ================== READ ================== */")
    tb.append(f"                found = 0;")
    tb.append(f"    ")
    tb.append(f"                repeat (5) begin")
    tb.append(f"                    try_idx = $urandom_range(0, 24);")
    tb.append(f"    ")
    tb.append(f"                    if (has_written[try_idx]) begin")
    tb.append(f"                        valid_idx   = try_idx;")
    tb.append(f"                        found       = 1;")
    tb.append(f"                    end")
    tb.append(f"                end")
    tb.append(f"    ")
    tb.append(f"                if (found) begin")
    tb.append(
        f'                    $display("[READ ] Addr = 0x%08h", addr_list[valid_idx]);'
    )
    tb.append(f"    ")
    tb.append(f"                    m0_read_addr    <= addr_list[valid_idx];")
    tb.append(f"                    m0_read_req     <= 1'b1;")
    tb.append(f"    ")
    tb.append(f"                    @(posedge m0_RREADY);")
    tb.append(f"                        m0_read_req <= 1'b0;")
    tb.append(f"                end else begin")
    tb.append(
        f'                    $display("[SKIP ] Tidak ada alamat yang valid untuk read");'
    )
    tb.append(f"                end")
    tb.append(f"            end")
    tb.append(f"    ")
    tb.append(f"            total_ops += 1;")
    tb.append(f"        end")
    tb.append(f"    ")
    tb.append(f'        $display("\\n[INFO] Selesai semua test random read-write\\n");')
    tb.append(f"        $finish;")
    tb.append(f"    end")
    tb.append(f"    ")

    tb.append(f"endmodule")

    return "\n".join(tb)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python tb_generator.py mXsY (e.g., m2s2)")
        sys.exit(1)

    try:
        m, s = parse_args(sys.argv[1])
        verilog_tb = generate_tb(m, s)
        output_dir = "logical/tb/tb_axi4_lite_interconnect"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/tb_axi4_lite_interconnect_m{m}s{s}.v"
        with open(filename, "w") as f:
            f.write(verilog_tb)
        print(f"generated: {filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
