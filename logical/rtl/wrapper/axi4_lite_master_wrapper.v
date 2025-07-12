module axi4_lite_master_wrapper #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32
) (
    input                               iCLK,
    input                               iRST,
    
    /* write address channel */
    input                               m_AWREADY,
    output                              m_AWVALID,
    output      [2:0]                   m_AWPROT,
    output      [ADDR_WIDTH-1:0]        m_AWADDR,
    
    /* write data channel */
    input                               m_WREADY,
    output                              m_WVALID,
    output      [DATA_WIDTH-1:0]        m_WDATA,
    output      [(DATA_WIDTH/8)-1:0]    m_WSTRB,
    
    /* write response channel */
    input                               m_BVALID,
    input       [1:0]                   m_BRESP,
    output                              m_BREADY,
    
    /* read address channel */
    input                               m_ARREADY,
    output                              m_ARVALID,
    output      [2:0]                   m_ARPROT,
    output      [ADDR_WIDTH-1:0]        m_ARADDR,
    
    /* read data channel */
    input                               m_RVALID,
    input       [1:0]                   m_RRESP,
    input       [DATA_WIDTH-1:0]        m_RDATA,
    output                              m_RREADY
);

    /* write interfaces */
    wire                            write_req, write_done;
    wire    [1:0]                   write_resp;
    wire    [(DATA_WIDTH/8)-1:0]    write_strb;
    wire    [ADDR_WIDTH-1:0]        write_addr;
    wire    [DATA_WIDTH-1:0]        write_data;
    reg                             write_done_reg;
    reg     [1:0]                   write_resp_reg;

    /* read interfaces */
    wire                            read_req, read_done;
    wire    [1:0]                   read_resp;
    wire    [ADDR_WIDTH-1:0]        read_addr;
    wire    [DATA_WIDTH-1:0]        read_data;
    reg                             read_done_reg;
    reg     [1:0]                   read_resp_reg;
    reg     [DATA_WIDTH-1:0]        read_data_reg;

    axi4_lite_master #(
        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)
    ) axi_master (
        .iCLK(iCLK), .iRST(iRST),
        
        /* write */
        .m_AWREADY(m_AWREADY), .m_AWVALID(m_AWVALID), .m_AWPROT(m_AWPROT), .m_AWADDR(m_AWADDR),
        .m_WREADY(m_WREADY), .m_WVALID(m_WVALID), .m_WDATA(m_WDATA), .m_WSTRB(m_WSTRB),
        .m_BVALID(m_BVALID), .m_BRESP(m_BRESP), .m_BREADY(m_BREADY),
        
        /* read */
        .m_ARREADY(m_ARREADY), .m_ARVALID(m_ARVALID), .m_ARPROT(m_ARPROT), .m_ARADDR(m_ARADDR),
        .m_RVALID(m_RVALID), .m_RRESP(m_RRESP), .m_RDATA(m_RDATA), .m_RREADY(m_RREADY),

        /* interface */
        .write_req(write_req), .write_addr(write_addr), .write_data(write_data), .write_strb(write_strb), .write_resp(write_resp),
        .read_req(read_req), .read_addr(read_addr), .read_data(read_data), .read_resp(read_resp)
    );

    /* logic */
    always @(posedge iCLK or negedge iRST) begin
        if (!iRST) begin
            write_done_reg      <= 1'b0;
            read_done_reg       <= 1'b0;

            write_resp_reg      <= {2{1'b0}};
            read_resp_reg       <= {2{1'b0}};
            read_data_reg       <= {DATA_WIDTH{1'b0}};
        end else begin
            write_done_reg      <= (m_BVALID && m_BREADY);
            read_done_reg       <= (m_RVALID && m_RREADY);

            if (m_BVALID && m_BREADY)     write_resp_reg    <= m_BRESP;
            if (m_RVALID && m_RREADY) begin
                read_resp_reg   <= m_RRESP;
                read_data_reg   <= m_RDATA;
            end
        end
    end

    /* assigns */
    assign write_strb   = {(DATA_WIDTH/8){1'b1}};

    assign write_done   = (m_BVALID && m_BREADY);
    assign read_done    = (m_RVALID && m_RREADY);

    /* intances */
        // intances your module here
        
endmodule