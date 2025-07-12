`timescale 1ns / 1ns

module tb_wrapper_axi4_lite_interconnect_m1s2();
    /* address parameters */
    parameter LOW_ADDR0     = 32'h00000000;
    parameter HIGH_ADDR0    = 32'h000000ff;
    parameter LOW_ADDR1     = 32'h00000100;
    parameter HIGH_ADDR1    = 32'h000001ff;

    parameter           CLK_PERIOD = 10;
    reg                 iCLK, iRST;

    /* master 0 signals */
    wire                m0_AWVALID, m0_AWREADY;
    wire    [31:0]      m0_AWADDR;

    wire                m0_WVALID, m0_WREADY;
    wire    [3:0]       m0_WSTRB;
    wire    [31:0]      m0_WDATA;

    wire                m0_BREADY, m0_BVALID;
    wire    [1:0]       m0_BRESP;

    wire                m0_ARVALID, m0_ARREADY;
    wire    [31:0]      m0_ARADDR;

    wire                m0_RREADY, m0_RVALID;
    wire    [1:0]       m0_RRESP;
    wire    [31:0]      m0_RDATA;


    /* slave 0 signals */
    wire                s0_AWVALID, s0_AWREADY;
    wire    [31:0]      s0_AWADDR;

    wire                s0_WVALID, s0_WREADY;
    wire    [3:0]       s0_WSTRB;
    wire    [31:0]      s0_WDATA;

    wire                s0_BREADY, s0_BVALID;
    wire    [1:0]       s0_BRESP;

    wire                s0_ARVALID, s0_ARREADY;
    wire    [31:0]      s0_ARADDR;

    wire                s0_RREADY, s0_RVALID;
    wire    [1:0]       s0_RRESP;
    wire    [31:0]      s0_RDATA;


    /* slave 1 signals */
    wire                s1_AWVALID, s1_AWREADY;
    wire    [31:0]      s1_AWADDR;

    wire                s1_WVALID, s1_WREADY;
    wire    [3:0]       s1_WSTRB;
    wire    [31:0]      s1_WDATA;

    wire                s1_BREADY, s1_BVALID;
    wire    [1:0]       s1_BRESP;

    wire                s1_ARVALID, s1_ARREADY;
    wire    [31:0]      s1_ARADDR;

    wire                s1_RREADY, s1_RVALID;
    wire    [1:0]       s1_RRESP;
    wire    [31:0]      s1_RDATA;


    /* master 0 */
    dut_axi4_lite_master_wrapper #(
        .ADDR_WIDTH(32), .DATA_WIDTH(32)
    ) master0 (
        .iCLK(iCLK), .iRST(iRST),

        /* write */
        .m_AWREADY(m0_AWREADY), .m_AWVALID(m0_AWVALID), .m_AWPROT(), .m_AWADDR(m0_AWADDR),
        .m_WREADY(m0_WREADY), .m_WVALID(m0_WVALID), .m_WDATA(m0_WDATA), .m_WSTRB(m0_WSTRB),
        .m_BVALID(m0_BVALID), .m_BRESP(m0_BRESP), .m_BREADY(m0_BREADY),

        /* read */
        .m_ARREADY(m0_ARREADY), .m_ARVALID(m0_ARVALID), .m_ARPROT(), .m_ARADDR(m0_ARADDR),
        .m_RVALID(m0_RVALID), .m_RRESP(m0_RRESP), .m_RDATA(m0_RDATA), .m_RREADY(m0_RREADY)
    );

    /* slave 0 */
    dut_axi4_lite_slave_wrapper #(
        .ADDR_WIDTH(32), .DATA_WIDTH(32)
    ) slave0 (
        .iCLK(iCLK), .iRST(iRST),

        /* write */
        .s_AWVALID(s0_AWVALID), .s_AWPROT(3'b0), .s_AWADDR(s0_AWADDR), .s_AWREADY(s0_AWREADY),
        .s_WVALID(s0_WVALID), .s_WDATA(s0_WDATA), .s_WSTRB(s0_WSTRB), .s_WREADY(s0_WREADY),
        .s_BREADY(s0_BREADY), .s_BVALID(s0_BVALID), .s_BRESP(s0_BRESP),

        /* read */
        .s_ARVALID(s0_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s0_ARADDR), .s_ARREADY(s0_ARREADY),
        .s_RREADY(s0_RREADY), .s_RVALID(s0_RVALID), .s_RRESP(s0_RRESP), .s_RDATA(s0_RDATA)
    );

    /* slave 1 */
    dut_axi4_lite_slave_wrapper #(
        .ADDR_WIDTH(32), .DATA_WIDTH(32)
    ) slave1 (
        .iCLK(iCLK), .iRST(iRST),

        /* write */
        .s_AWVALID(s1_AWVALID), .s_AWPROT(3'b0), .s_AWADDR(s1_AWADDR), .s_AWREADY(s1_AWREADY),
        .s_WVALID(s1_WVALID), .s_WDATA(s1_WDATA), .s_WSTRB(s1_WSTRB), .s_WREADY(s1_WREADY),
        .s_BREADY(s1_BREADY), .s_BVALID(s1_BVALID), .s_BRESP(s1_BRESP),

        /* read */
        .s_ARVALID(s1_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s1_ARADDR), .s_ARREADY(s1_ARREADY),
        .s_RREADY(s1_RREADY), .s_RVALID(s1_RVALID), .s_RRESP(s1_RRESP), .s_RDATA(s1_RDATA)
    );

    /* interconnect */
    axi4_lite_interconnect_m1s2 #(
        .LOW_ADDR0(LOW_ADDR0), .HIGH_ADDR0(HIGH_ADDR0),
        .LOW_ADDR1(LOW_ADDR1), .HIGH_ADDR1(HIGH_ADDR1)
    ) interconnect (
        .iCLK(iCLK), .iRST(iRST),

        /* master 0 signals */
        .m0_AWVALID(m0_AWVALID), .m0_AWADDR(m0_AWADDR), .m0_AWREADY(m0_AWREADY),
        .m0_WVALID(m0_WVALID), .m0_WSTRB(m0_WSTRB), .m0_WDATA(m0_WDATA), .m0_WREADY(m0_WREADY),
        .m0_BREADY(m0_BREADY), .m0_BVALID(m0_BVALID), .m0_BRESP(m0_BRESP),
        .m0_ARVALID(m0_ARVALID), .m0_ARADDR(m0_ARADDR), .m0_ARREADY(m0_ARREADY),
        .m0_RREADY(m0_RREADY), .m0_RVALID(m0_RVALID), .m0_RRESP(m0_RRESP), .m0_RDATA(m0_RDATA),

        /* slave 0 signals */
        .s0_AWREADY(s0_AWREADY), .s0_AWVALID(s0_AWVALID), .s0_AWADDR(s0_AWADDR),
        .s0_WREADY(s0_WREADY), .s0_WVALID(s0_WVALID), .s0_WSTRB(s0_WSTRB), .s0_WDATA(s0_WDATA),
        .s0_BVALID(s0_BVALID), .s0_BRESP(s0_BRESP), .s0_BREADY(s0_BREADY),
        .s0_ARREADY(s0_ARREADY), .s0_ARVALID(s0_ARVALID), .s0_ARADDR(s0_ARADDR),
        .s0_RVALID(s0_RVALID), .s0_RRESP(s0_RRESP), .s0_RDATA(s0_RDATA), .s0_RREADY(s0_RREADY),

        /* slave 1 signals */
        .s1_AWREADY(s1_AWREADY), .s1_AWVALID(s1_AWVALID), .s1_AWADDR(s1_AWADDR),
        .s1_WREADY(s1_WREADY), .s1_WVALID(s1_WVALID), .s1_WSTRB(s1_WSTRB), .s1_WDATA(s1_WDATA),
        .s1_BVALID(s1_BVALID), .s1_BRESP(s1_BRESP), .s1_BREADY(s1_BREADY),
        .s1_ARREADY(s1_ARREADY), .s1_ARVALID(s1_ARVALID), .s1_ARADDR(s1_ARADDR),
        .s1_RVALID(s1_RVALID), .s1_RRESP(s1_RRESP), .s1_RDATA(s1_RDATA), .s1_RREADY(s1_RREADY)
    );

    initial begin
        iCLK = 1'b1;
        forever #(CLK_PERIOD/2) iCLK = ~iCLK;
    end

    initial begin
        $dumpfile("logical/sim/wrapper/wrapper_axi4_lite_interconnect_m1s2.vcd");
        $dumpvars(0, tb_wrapper_axi4_lite_interconnect_m1s2);

        iCLK = 1; iRST = 0;
        #10; iRST = 1;

        #300; $finish;
    end

endmodule