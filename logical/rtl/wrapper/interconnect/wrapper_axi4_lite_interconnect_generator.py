import sys
import os


def parse_args(arg):
    if not arg.startswith("m") or "s" not in arg:
        raise ValueError("Format must be 'm{n}s{n}', example: m2s1")
    m_part, s_part = arg[1:].split("s")
    return int(m_part), int(s_part)


def generate_wrapper(m, s):
    wrapper = []

    # header
    wrapper.append(f"module wrapper_axi4_lite_interconnect_m{m}s{s} #(")

    # parameters
    wrapper.append(f"    /* parameters */")
    wrapper.append("    parameter ADDR_WIDTH    = 32,")
    wrapper.append("    parameter DATA_WIDTH    = 32")
    wrapper.append("")

    # generate address parameters for each slave
    wrapper.append(f"    /* address parameters */")
    for i in range(s):
        wrapper.append(f"    parameter LOW_ADDR{i}     = 32'h{i:04x}_0000,")
        wrapper.append(
            f"    parameter HIGH_ADDR{i}    = 32'h{i:04x}_FFFF{',' if i != s-1 else ''}"
        )

    wrapper.append(") (")

    wrapper.append(f"    /* input */")
    wrapper.append(f"    input                           iCLK, iRST,")
    wrapper.append(f"")
    wrapper.append(f"    /* output */")
    wrapper.append(f"    output  [ADDR_WIDTH-1:0]        ADDR,")
    wrapper.append(f"    output  [DATA_WIDTH-1:0]        DATA")
    wrapper.append(f");")
    wrapper.append(f"    ")

    # master signals
    for master in range(m):
        wrapper.append(f"    /* master {master} signals */")
        wrapper.append(
            f"    wire                            m{master}_AWVALID, m{master}_AWREADY;"
        )
        wrapper.append(f"    wire    [ADDR_WIDTH-1:0]        m{master}_AWADDR;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            m{master}_WVALID, m{master}_WREADY;"
        )
        wrapper.append(f"    wire    [(DATA_WIDTH/8)-1:0]    m{master}_WSTRB;")
        wrapper.append(f"    wire    [DATA_WIDTH-1:0]        m{master}_WDATA;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            m{master}_BREADY, m{master}_BVALID;"
        )
        wrapper.append(f"    wire    [1:0]                   m{master}_BRESP;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            m{master}_ARVALID, m{master}_ARREADY;"
        )
        wrapper.append(f"    wire    [ADDR_WIDTH-1:0]        m{master}_ARADDR;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            m{master}_RREADY, m{master}_RVALID;"
        )
        wrapper.append(f"    wire    [1:0]                   m{master}_RRESP;")
        wrapper.append(f"    wire    [DATA_WIDTH-1:0]        m{master}_RDATA;")
        wrapper.append(f"    ")
        wrapper.append(f"    ")

    # slave signals
    for slave in range(s):
        wrapper.append(f"    /* slave {slave} signals */")
        wrapper.append(
            f"    wire                            s{slave}_AWVALID, s{slave}_AWREADY;"
        )
        wrapper.append(f"    wire    [ADDR_WIDTH-1:0]        s{slave}_AWADDR;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            s{slave}_WVALID, s{slave}_WREADY;"
        )
        wrapper.append(f"    wire    [(DATA_WIDTH/8)-1:0]    s{slave}_WSTRB;")
        wrapper.append(f"    wire    [DATA_WIDTH-1:0]        s{slave}_WDATA;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            s{slave}_BREADY, s{slave}_BVALID;"
        )
        wrapper.append(f"    wire    [1:0]                   s{slave}_BRESP;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            s{slave}_ARVALID, s{slave}_ARREADY;"
        )
        wrapper.append(f"    wire    [ADDR_WIDTH-1:0]        s{slave}_ARADDR;")
        wrapper.append(f"    ")
        wrapper.append(
            f"    wire                            s{slave}_RREADY, s{slave}_RVALID;"
        )
        wrapper.append(f"    wire    [1:0]                   s{slave}_RRESP;")
        wrapper.append(f"    wire    [DATA_WIDTH-1:0]        s{slave}_RDATA;")
        wrapper.append(f"    ")
        wrapper.append(f"    ")

    # instantiate masters
    for master in range(m):
        wrapper.append(f"    axi4_lite_master_wrapper #(")
        wrapper.append(f"        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)")
        wrapper.append(f"    ) master{master} (")
        wrapper.append(f"        .iCLK(iCLK), .iRST(iRST),")
        wrapper.append(f"        ")
        wrapper.append("        /* write */")
        wrapper.append(
            f"        .m_AWREADY(m{master}_AWREADY), .m_AWVALID(m{master}_AWVALID), .m_AWPROT(), .m_AWADDR(m{master}_AWADDR),"
        )
        wrapper.append(
            f"        .m_WREADY(m{master}_WREADY), .m_WVALID(m{master}_WVALID), .m_WDATA(m{master}_WDATA), .m_WSTRB(m{master}_WSTRB),"
        )
        wrapper.append(
            f"        .m_BVALID(m{master}_BVALID), .m_BRESP(m{master}_BRESP), .m_BREADY(m{master}_BREADY),"
        )
        wrapper.append(f"        ")
        wrapper.append("        /* read */")
        wrapper.append(
            f"        .m_ARREADY(m{master}_ARREADY), .m_ARVALID(m{master}_ARVALID), .m_ARPROT(), .m_ARADDR(m{master}_ARADDR),"
        )
        wrapper.append(
            f"        .m_RVALID(m{master}_RVALID), .m_RRESP(m{master}_RRESP), .m_RDATA(m{master}_RDATA), .m_RREADY(m{master}_RREADY)"
        )
        wrapper.append(f"    );")
        wrapper.append(f"    ")

    # instantiate slaves
    for slave in range(s):
        wrapper.append(f"    axi4_lite_slave_wrapper #(")
        wrapper.append(f"        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)")
        wrapper.append(f"    ) slave{slave} (")
        wrapper.append(f"        .iCLK(iCLK), .iRST(iRST),")
        wrapper.append(f"        ")
        wrapper.append("        /* write */")
        wrapper.append(
            f"        .s_AWVALID(s{slave}_AWVALID), .s_AWPROT(3'b0), .s_AWADDR(s{slave}_AWADDR), .s_AWREADY(s{slave}_AWREADY),"
        )
        wrapper.append(
            f"        .s_WVALID(s{slave}_WVALID), .s_WDATA(s{slave}_WDATA), .s_WSTRB(s{slave}_WSTRB), .s_WREADY(s{slave}_WREADY),"
        )
        wrapper.append(
            f"        .s_BREADY(s{slave}_BREADY), .s_BVALID(s{slave}_BVALID), .s_BRESP(s{slave}_BRESP),"
        )
        wrapper.append(f"        ")
        wrapper.append("        /* read */")
        wrapper.append(
            f"        .s_ARVALID(s{slave}_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s{slave}_ARADDR), .s_ARREADY(s{slave}_ARREADY),"
        )
        wrapper.append(
            f"        .s_RREADY(s{slave}_RREADY), .s_RVALID(s{slave}_RVALID), .s_RRESP(s{slave}_RRESP), .s_RDATA(s{slave}_RDATA)"
        )
        wrapper.append(f"    );")
        wrapper.append(f"    ")

    # instantiate interconnect
    wrapper.append(f"    axi4_lite_interconnect_m{m}s{s} #(")
    for slave in range(s):
        wrapper.append(
            f"        .LOW_ADDR{slave}(LOW_ADDR{slave}), .HIGH_ADDR{slave}(HIGH_ADDR{slave}){',' if slave != s-1 else ''}"
        )
    wrapper.append(f"    ) interconnect (")
    wrapper.append(f"        .iCLK(iCLK), .iRST(iRST),")
    wrapper.append(f"        ")

    # master connections
    for master in range(m):
        wrapper.append(f"        /* master {master} signals */")
        wrapper.append(
            f"        .m{master}_AWVALID(m{master}_AWVALID), .m{master}_AWADDR(m{master}_AWADDR), .m{master}_AWREADY(m{master}_AWREADY),"
        )
        wrapper.append(
            f"        .m{master}_WVALID(m{master}_WVALID), .m{master}_WSTRB(m{master}_WSTRB), .m{master}_WDATA(m{master}_WDATA), .m{master}_WREADY(m{master}_WREADY),"
        )
        wrapper.append(
            f"        .m{master}_BREADY(m{master}_BREADY), .m{master}_BVALID(m{master}_BVALID), .m{master}_BRESP(m{master}_BRESP),"
        )
        wrapper.append(
            f"        .m{master}_ARVALID(m{master}_ARVALID), .m{master}_ARADDR(m{master}_ARADDR), .m{master}_ARREADY(m{master}_ARREADY),"
        )
        wrapper.append(
            f"        .m{master}_RREADY(m{master}_RREADY), .m{master}_RVALID(m{master}_RVALID), .m{master}_RRESP(m{master}_RRESP), .m{master}_RDATA(m{master}_RDATA){',' if master != m-1 or s > 0 else ''}"
        )
        wrapper.append(f"        ")

    # slave connections
    for slave in range(s):
        wrapper.append(f"        /* slave {slave} signals */")
        wrapper.append(
            f"        .s{slave}_AWREADY(s{slave}_AWREADY), .s{slave}_AWVALID(s{slave}_AWVALID), .s{slave}_AWADDR(s{slave}_AWADDR),"
        )
        wrapper.append(
            f"        .s{slave}_WREADY(s{slave}_WREADY), .s{slave}_WVALID(s{slave}_WVALID), .s{slave}_WSTRB(s{slave}_WSTRB), .s{slave}_WDATA(s{slave}_WDATA),"
        )
        wrapper.append(
            f"        .s{slave}_BVALID(s{slave}_BVALID), .s{slave}_BRESP(s{slave}_BRESP), .s{slave}_BREADY(s{slave}_BREADY),"
        )
        wrapper.append(
            f"        .s{slave}_ARREADY(s{slave}_ARREADY), .s{slave}_ARVALID(s{slave}_ARVALID), .s{slave}_ARADDR(s{slave}_ARADDR), "
        )
        wrapper.append(
            f"        .s{slave}_RVALID(s{slave}_RVALID), .s{slave}_RRESP(s{slave}_RRESP), .s{slave}_RDATA(s{slave}_RDATA), .s{slave}_RREADY(s{slave}_RREADY)"
            + (",\n" if slave != s - 1 else "")
        )

    wrapper.append(f"    );")
    wrapper.append(f"    ")

    wrapper.append(f"endmodule")

    return "\n".join(wrapper)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python wrapper_generator.py mXsY (e.g., m2s2)")
        sys.exit(1)

    try:
        m, s = parse_args(sys.argv[1])
        verilog_wrapper = generate_wrapper(m, s)
        output_dir = "logical/rtl/wrapper/interconnect"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/wrapper_axi4_lite_interconnect_m{m}s{s}.v"
        with open(filename, "w") as f:
            f.write(verilog_wrapper)
        print(f"generated: {filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
