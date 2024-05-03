from pytoniq import LiteBalancer, begin_cell, Address


class Provider:
    def __init__(self):
        self.provider = LiteBalancer.from_mainnet_config(1)

    async def get_jetton_wallet_address(self, jetton_master_address: str, address: str) -> Address:
        await self.provider.start_up()

        result_stack = await self.provider.run_get_method(
            address=jetton_master_address,
            method='get_wallet_address',
            stack=[
                begin_cell()
                .store_address(address)
                .end_cell()
                .begin_parse()
            ]
        )

        jetton_wallet_address = result_stack[0].load_address()

        await self.provider.close_all()

        return jetton_wallet_address
