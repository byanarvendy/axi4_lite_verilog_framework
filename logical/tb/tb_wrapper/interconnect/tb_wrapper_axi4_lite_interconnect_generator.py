import sys
import os


def parse_args(arg):
    if not arg.startswith("m") or "s" not in arg:
        raise ValueError("Format must be 'm{n}s{n}', example: m2s1")
    m_part, s_part = arg[1:].split("s")
    return int(m_part), int(s_part)


def generate_tb(m, s):
    tb = []

    # header
    tb.append("`timescale 1ns / 1ns\n")
    tb.append(f"module tb_wrapper_axi4_lite_interconnect_m{m}s{s}();")

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

    # master signals
    for master in range(m):
        tb.append(f"    /* master {master} signals */")
        tb.append(f"    wire                m{master}_AWVALID, m{master}_AWREADY;")
        tb.append(f"    wire    [31:0]      m{master}_AWADDR;")
        tb.append("")
        tb.append(f"    wire                m{master}_WVALID, m{master}_WREADY;")
        tb.append(f"    wire    [3:0]       m{master}_WSTRB;")
        tb.append(f"    wire    [31:0]      m{master}_WDATA;")
        tb.append("")
        tb.append(f"    wire                m{master}_BREADY, m{master}_BVALID;")
        tb.append(f"    wire    [1:0]       m{master}_BRESP;")
        tb.append("")
        tb.append(f"    wire                m{master}_ARVALID, m{master}_ARREADY;")
        tb.append(f"    wire    [31:0]      m{master}_ARADDR;")
        tb.append("")
        tb.append(f"    wire                m{master}_RREADY, m{master}_RVALID;")
        tb.append(f"    wire    [1:0]       m{master}_RRESP;")
        tb.append(f"    wire    [31:0]      m{master}_RDATA;")
        tb.append("")
        tb.append("")

    # slave signals
    for slave in range(s):
        tb.append(f"    /* slave {slave} signals */")
        tb.append(f"    wire                s{slave}_AWVALID, s{slave}_AWREADY;")
        tb.append(f"    wire    [31:0]      s{slave}_AWADDR;")
        tb.append("")
        tb.append(f"    wire                s{slave}_WVALID, s{slave}_WREADY;")
        tb.append(f"    wire    [3:0]       s{slave}_WSTRB;")
        tb.append(f"    wire    [31:0]      s{slave}_WDATA;")
        tb.append("")
        tb.append(f"    wire                s{slave}_BREADY, s{slave}_BVALID;")
        tb.append(f"    wire    [1:0]       s{slave}_BRESP;")
        tb.append("")
        tb.append(f"    wire                s{slave}_ARVALID, s{slave}_ARREADY;")
        tb.append(f"    wire    [31:0]      s{slave}_ARADDR;")
        tb.append("")
        tb.append(f"    wire                s{slave}_RREADY, s{slave}_RVALID;")
        tb.append(f"    wire    [1:0]       s{slave}_RRESP;")
        tb.append(f"    wire    [31:0]      s{slave}_RDATA;")
        tb.append("")
        tb.append("")

    # master instances
    for master in range(m):
        tb.append(f"    /* master {master} */")
        tb.append(f"    dut_axi4_lite_master_wrapper #(")
        tb.append(f"        .ADDR_WIDTH(32), .DATA_WIDTH(32)")
        tb.append(f"    ) master{master} (")
        tb.append(f"        .iCLK(iCLK), .iRST(iRST),")
        tb.append("")
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
        tb.append("")
        tb.append("        /* read */")
        tb.append(
            f"        .m_ARREADY(m{master}_ARREADY), .m_ARVALID(m{master}_ARVALID), .m_ARPROT(), .m_ARADDR(m{master}_ARADDR),"
        )
        tb.append(
            f"        .m_RVALID(m{master}_RVALID), .m_RRESP(m{master}_RRESP), .m_RDATA(m{master}_RDATA), .m_RREADY(m{master}_RREADY)"
        )
        tb.append("    );")
        tb.append("")

    # Slave instances
    for slave in range(s):
        tb.append(f"    /* slave {slave} */")
        tb.append(f"    dut_axi4_lite_slave_wrapper #(")
        tb.append(f"        .ADDR_WIDTH(32), .DATA_WIDTH(32)")
        tb.append(f"    ) slave{slave} (")
        tb.append(f"        .iCLK(iCLK), .iRST(iRST),")
        tb.append("")
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
        tb.append("")
        tb.append("        /* read */")
        tb.append(
            f"        .s_ARVALID(s{slave}_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s{slave}_ARADDR), .s_ARREADY(s{slave}_ARREADY),"
        )
        tb.append(
            f"        .s_RREADY(s{slave}_RREADY), .s_RVALID(s{slave}_RVALID), .s_RRESP(s{slave}_RRESP), .s_RDATA(s{slave}_RDATA)"
        )
        tb.append("    );")
        tb.append("")

    # interconnect instance
    tb.append("    /* interconnect */")
    tb.append(f"    axi4_lite_interconnect_m{m}s{s} #(")
    for slave in range(s):
        tb.append(
            f"        .LOW_ADDR{slave}(LOW_ADDR{slave}), .HIGH_ADDR{slave}(HIGH_ADDR{slave}){',' if slave != s-1 else ''}"
        )
    tb.append("    ) interconnect (")
    tb.append("        .iCLK(iCLK), .iRST(iRST),")
    tb.append("")

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
        tb.append("")

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
            f"        .s{slave}_ARREADY(s{slave}_ARREADY), .s{slave}_ARVALID(s{slave}_ARVALID), .s{slave}_ARADDR(s{slave}_ARADDR),"
        )
        tb.append(
            f"        .s{slave}_RVALID(s{slave}_RVALID), .s{slave}_RRESP(s{slave}_RRESP), .s{slave}_RDATA(s{slave}_RDATA), .s{slave}_RREADY(s{slave}_RREADY)"
            + (",\n" if slave != s - 1 else "")
        )

    tb.append("    );")
    tb.append("")

    # clock generation
    tb.append("    initial begin")
    tb.append("        iCLK = 1'b1;")
    tb.append("        forever #(CLK_PERIOD/2) iCLK = ~iCLK;")
    tb.append("    end")
    tb.append("")

    # test sequence
    tb.append("    initial begin")
    tb.append(
        f'        $dumpfile("logical/sim/wrapper/wrapper_axi4_lite_interconnect_m{m}s{s}.vcd");'
    )
    tb.append(f"        $dumpvars(0, tb_wrapper_axi4_lite_interconnect_m{m}s{s});")
    tb.append("")
    tb.append("        iCLK = 1; iRST = 0;")
    tb.append("        #10; iRST = 1;")
    tb.append("")
    tb.append("        #300; $finish;")
    tb.append("    end")
    tb.append("")
    tb.append("endmodule")

    return "\n".join(tb)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python tb_generator.py mXsY (e.g., m2s2)")
        sys.exit(1)

    try:
        m, s = parse_args(sys.argv[1])
        verilog_tb = generate_tb(m, s)
        output_dir = "logical/tb/tb_wrapper/interconnect"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/tb_wrapper_axi4_lite_interconnect_m{m}s{s}.v"
        with open(filename, "w") as f:
            f.write(verilog_tb)
        print(f"generated: {filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
