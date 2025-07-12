module axi4_lite_master #(
    parameter ADDR_WIDTH    = 32,
    parameter DATA_WIDTH    = 32
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
    output                              m_RREADY,
    
    /* wire interface */
    input                               write_req,
    input       [ADDR_WIDTH-1:0]        write_addr,
    input       [DATA_WIDTH-1:0]        write_data,
    input       [(DATA_WIDTH/8)-1:0]    write_strb,
    output      [1:0]                   write_resp,

    /* read interface */
    input                               read_req,
    input       [ADDR_WIDTH-1:0]        read_addr,
    output      [DATA_WIDTH-1:0]        read_data,
    output      [1:0]                   read_resp
);

    /* protection bits */
    assign m_AWPROT     = 3'b000;
    assign m_ARPROT     = 3'b000;
    
    /* finite state machine */
    localparam IDLE     = 3'b000;
    localparam WADDR    = 3'b001;
    localparam WDATA    = 3'b010;
    localparam WRESP    = 3'b011;
    localparam RADDR    = 3'b100;
    localparam RDATA    = 3'b101;

    reg         read_start, write_start;
    reg [2:0]   state, next_state;

    always @(posedge iCLK or negedge iRST) begin
        if (!iRST) begin
            state           <= IDLE;
            write_start     <= 1'b0;
            read_start      <= 1'b0;
        end else begin
            state           <= next_state;
            write_start     <= write_req;
            read_start      <= read_req;
        end
    end

    always @(*) begin
        next_state = state;
        case (state)
            IDLE: next_state = (write_req) ? WADDR : ((read_req) ? RADDR : IDLE);
            WADDR: if (m_AWVALID && m_AWREADY)  next_state  = WDATA;
            WDATA: if (m_WVALID  && m_WREADY)   next_state  = WRESP;
            WRESP: if (m_BVALID  && m_BREADY)   next_state  = IDLE;
            RADDR: if (m_ARVALID && m_ARREADY)  next_state  = RDATA;
            RDATA: if (m_RVALID  && m_RREADY)   next_state  = IDLE;
        endcase
    end

    /* write request */
    assign m_AWVALID    = (state == WADDR) ? 1'b1           : 1'b0;
    assign m_AWADDR     = (state == WADDR) ? write_addr     : {ADDR_WIDTH{1'b0}};

    /* write data */
    assign m_WVALID     = (state == WDATA) ? 1'b1           : 1'b0;
    assign m_WDATA      = (state == WDATA) ? write_data     : {DATA_WIDTH{1'b0}};
    assign m_WSTRB      = (state == WDATA) ? write_strb     : {(DATA_WIDTH/8){1'b0}};

    /* write response */
    assign m_BREADY     = (state == WRESP) ? 1'b1           : 1'b0;
    assign write_resp   = (state == WRESP) ? m_BRESP        : {2{1'b0}};

    /* read request */
    assign m_ARVALID    = (state == RADDR) ? 1'b1           : 1'b0;
    assign m_ARADDR     = (state == RADDR) ? read_addr      : {ADDR_WIDTH{1'b0}};

    /* read data */
    assign m_RREADY     = (state == RDATA) ? 1'b1           : 1'b0;
    assign read_data    = (state == RDATA) ? m_RDATA        : {DATA_WIDTH{1'b0}};
    assign read_resp    = (state == RDATA) ? m_RRESP        : {2{1'b0}};

endmodule
