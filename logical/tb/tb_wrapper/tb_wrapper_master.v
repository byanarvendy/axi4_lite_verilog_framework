`timescale 1ns / 1ps

module tb_master();
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;

    reg iCLK, iRST;

    reg                     m_AWREADY;
    wire [2:0]              m_AWPROT;
    wire                    m_AWVALID;
    wire [ADDR_WIDTH-1:0]   m_AWADDR;

    reg                     m_WREADY;
    wire                    m_WVALID;
    wire [DATA_WIDTH-1:0]   m_WDATA;
    wire [(DATA_WIDTH/8)-1:0] m_WSTRB;

    reg                     m_BVALID;
    reg [1:0]               m_BRESP;
    wire                    m_BREADY;

    reg                     m_ARREADY;
    wire [2:0]              m_ARPROT;
    wire                    m_ARVALID;
    wire [ADDR_WIDTH-1:0]   m_ARADDR;

    reg                     m_RVALID;
    reg [1:0]               m_RRESP;
    reg [DATA_WIDTH-1:0]    m_RDATA;
    wire                    m_RREADY;

    dut_axi4_lite_master_wrapper #(
        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)
    ) dut (
        .iCLK(iCLK), .iRST(iRST),
        .m_AWREADY(m_AWREADY), .m_AWPROT(m_AWPROT), .m_AWVALID(m_AWVALID), .m_AWADDR(m_AWADDR),
        .m_WREADY(m_WREADY), .m_WVALID(m_WVALID), .m_WDATA(m_WDATA), .m_WSTRB(m_WSTRB),
        .m_BVALID(m_BVALID), .m_BRESP(m_BRESP), .m_BREADY(m_BREADY),
        .m_ARREADY(m_ARREADY), .m_ARPROT(m_ARPROT), .m_ARVALID(m_ARVALID), .m_ARADDR(m_ARADDR),
        .m_RVALID(m_RVALID), .m_RRESP(m_RRESP), .m_RDATA(m_RDATA), .m_RREADY(m_RREADY)
    );

    always #5 iCLK = ~iCLK;

    initial begin
        $dumpfile("logical/sim/wrapper/tb_master.vcd");
        $dumpvars(0, tb_master);

        iCLK = 1; iRST = 0;
        #10; iRST = 1;

        #300; $finish;
    end

endmodule