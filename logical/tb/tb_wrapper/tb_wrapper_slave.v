`timescale 1ns / 1ps

module tb_slave();
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;

    reg iCLK, iRST;

    wire                    s_AWREADY;
    wire [2:0]              s_AWPROT;
    wire                    s_AWVALID;
    wire [ADDR_WIDTH-1:0]   s_AWADDR;

    wire                    s_WREADY;
    wire                    s_WVALID;
    wire [DATA_WIDTH-1:0]   s_WDATA;
    wire [(DATA_WIDTH/8)-1:0] s_WSTRB;

    wire                    s_BVALID;
    wire [1:0]              s_BRESP;
    wire                    s_BREADY;

    wire                    s_ARREADY;
    wire [2:0]              s_ARPROT;
    wire                    s_ARVALID;
    wire [ADDR_WIDTH-1:0]   s_ARADDR;

    wire                    s_RVALID;
    wire [1:0]              s_RRESP;
    wire [DATA_WIDTH-1:0]   s_RDATA;
    wire                    s_RREADY;

    dut_axi4_lite_slave_wrapper #(
        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)
    ) dut (
        .iCLK(iCLK), .iRST(iRST),
        .s_AWREADY(s_AWREADY), .s_AWPROT(s_AWPROT), .s_AWVALID(s_AWVALID), .s_AWADDR(s_AWADDR),
        .s_WREADY(s_WREADY), .s_WVALID(s_WVALID), .s_WDATA(s_WDATA), .s_WSTRB(s_WSTRB),
        .s_BVALID(s_BVALID), .s_BRESP(s_BRESP), .s_BREADY(s_BREADY),
        .s_ARREADY(s_ARREADY), .s_ARPROT(s_ARPROT), .s_ARVALID(s_ARVALID), .s_ARADDR(s_ARADDR),
        .s_RVALID(s_RVALID), .s_RRESP(s_RRESP), .s_RDATA(s_RDATA), .s_RREADY(s_RREADY)
    );

    always #5 iCLK = ~iCLK;

    initial begin
        $dumpfile("logical/sim/wrapper/tb_slave.vcd");
        $dumpvars(0, tb_slave);

        iCLK = 1; iRST = 0;
        #10; iRST = 1;

        #300; $finish;
    end

endmodule