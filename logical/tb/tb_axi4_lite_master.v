`timescale 1ns / 1ps

module tb_axi4_lite_master();
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;

    reg iCLK, iRST;

    reg                         m_AWREADY;
    wire [2:0]                  m_AWPROT;
    wire                        m_AWVALID;
    wire [ADDR_WIDTH-1:0]       m_AWADDR;

    reg                         m_WREADY;
    wire                        m_WVALID;
    wire [DATA_WIDTH-1:0]       m_WDATA;
    wire [(DATA_WIDTH/8)-1:0]   m_WSTRB;

    reg                         m_BVALID;
    reg [1:0]                   m_BRESP;
    wire                        m_BREADY;

    reg                         m_ARREADY;
    wire [2:0]                  m_ARPROT;
    wire                        m_ARVALID;
    wire [ADDR_WIDTH-1:0]       m_ARADDR;

    reg                         m_RVALID;
    reg [1:0]                   m_RRESP;
    reg [DATA_WIDTH-1:0]        m_RDATA;
    wire                        m_RREADY;

    reg                         write_req;
    reg [ADDR_WIDTH-1:0]        write_addr;
    reg [DATA_WIDTH-1:0]        write_data;
    reg [(DATA_WIDTH/8)-1:0]    write_strb;
    wire                        write_done;
    wire [1:0]                  write_resp;

    reg                         read_req = 0;
    reg [ADDR_WIDTH-1:0]        read_addr = 0;
    wire [DATA_WIDTH-1:0]       read_data;
    wire                        read_done;
    wire [1:0]                  read_resp;

    axi4_lite_master #(
        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)
    ) dut (
        /* clock and reset */
        .iCLK(iCLK), .iRST(iRST),

        /* write */
        .m_AWREADY(m_AWREADY), .m_AWPROT(m_AWPROT), .m_AWVALID(m_AWVALID), .m_AWADDR(m_AWADDR),
        .m_WREADY(m_WREADY), .m_WVALID(m_WVALID), .m_WDATA(m_WDATA), .m_WSTRB(m_WSTRB),
        .m_BVALID(m_BVALID), .m_BRESP(m_BRESP), .m_BREADY(m_BREADY),

        /* read */
        .m_ARREADY(m_ARREADY), .m_ARPROT(m_ARPROT), .m_ARVALID(m_ARVALID), .m_ARADDR(m_ARADDR),
        .m_RVALID(m_RVALID), .m_RRESP(m_RRESP), .m_RDATA(m_RDATA), .m_RREADY(m_RREADY),

        /* interface */
        .write_req(write_req), .write_addr(write_addr), .write_data(write_data), .write_strb(write_strb), .write_done(write_done), .write_resp(write_resp),
        .read_req(read_req), .read_addr(read_addr), .read_data(read_data), .read_done(read_done), .read_resp(read_resp)
    );

    always #5 iCLK = ~iCLK;

    initial begin
        $dumpfile("logical/sim/tb_axi4_lite_master.vcd");
        $dumpvars(0, tb_axi4_lite_master);

        iCLK = 1;
        iRST = 0;
        m_AWREADY = 0;
        m_WREADY = 0;
        m_BVALID = 0;
        m_BRESP = 2'b00;
        m_ARREADY = 0;
        m_RVALID = 0;
        m_RRESP = 2'b00;
        m_RDATA = 0;

        write_req = 0;
        write_addr = 0;
        write_data = 0;
        write_strb = 4'b1111;


        #10; iRST = 1;

        // #20;
        //     write_addr = 32'h0000_0004;
        //     write_data = 32'hDEAD_BEEF;
        //     write_req  = 1;

        // #10;
        //     write_req  = 0;
        //     m_AWREADY = 1;
        //     m_WREADY = 1;
        //     m_BVALID = 1;

        // #30;
        //     m_AWREADY = 0;
        //     m_WREADY = 0;
        //     write_addr = 32'h0000_0000;
        //     write_data = 32'h0000_0000;

        // #10;
        //     m_BVALID = 0;
        //     write_req  = 1;
        //     write_addr = 32'h0000_240;
        //     write_data = 32'h0456_0FED;     

        // #10;
        //     m_AWREADY = 1;
        //     m_WREADY = 1;
        //     m_BVALID = 1;

        // #20;
        //     m_AWREADY = 0;
        //     m_WREADY = 0;
        //     write_req  = 0;
        //     write_addr = 32'h0000_0000;
        //     write_data = 32'h0000_0000;

        #50;
            read_req = 1;
            read_addr = 32'h0000_0004;
        
        #10;
            m_ARREADY = 1;
        
        #10;
            m_ARREADY = 0;
            m_RVALID = 1;
            m_RDATA = 32'hDEAD_BEEF;

        #10;
            m_RVALID = 0;
            read_req = 0;
            read_addr = 32'h0000_0000;
            m_RDATA = 32'h0000_0000;
            
        #50;
        $finish;
    end

endmodule
