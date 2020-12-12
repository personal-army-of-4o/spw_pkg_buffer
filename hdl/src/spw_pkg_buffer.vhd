-- this block ensures stream sink wont pull the start of the next pkg in a hurry
-- fsm jist:
-- 1. set out handshake high
-- 2. wait for input handshake high
-- 3. connect data interfaces so that stream sink coul pull data from source
-- 4. wait for EOP or EEP, set oAck low the next tick EOP or EEP was handed to sink
-- 5. set out handshake low
-- 6. wait for in handshake low
-- 7. go to 1
--
-- dont forget to handle exceptions in all fsm states

library ieee;
use ieee.std_logic_1164.all;


entity spw_pkg_buffer is
    port (
        iClk: in std_logic;
        iReset: in std_logic;

        -- from data source
        iValid: in std_logic;
        iData: in std_logic_vector (8 downto 0);
        oAck: out std_logic;

        -- control
        oHandshake: out std_logic;
        iHandshake: in std_logic;

        -- to data sink
        oValid: out std_logic;
        oData: out std_logic_vector (8 downto 0);
        iAck: in std_logic
    );
end entity;

architecture v1 of spw_pkg_buffer is
begin
end v1;