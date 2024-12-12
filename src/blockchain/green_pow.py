class GreenProofOfWork:
    def __init__(self, initial_difficulty=4, target_block_time=60, adjustment_interval=10):
        self.difficulty = initial_difficulty
        self.target_block_time = target_block_time
        self.adjustment_interval = adjustment_interval
        self.block_times = []
        self.carbon_credits: Dict[str, float] = {}
        self.renewable_energy_sources = ["solar", "wind", "hydro", "geothermal"]

    def mine(self, block_data: str, miner_address: str):
        nonce = 0
        start_time = time.time()
        target = "0" * self.difficulty
        energy_source = random.choice(self.renewable_energy_sources)
        while True:
            block_hash = self.calculate_hash(block_data, nonce, energy_source)
            if block_hash.startswith(target):
                end_time = time.time()
                self.block_times.append(end_time - start_time)
                self.adjust_difficulty()
                self.award_carbon_credits(miner_address, energy_source)
                return nonce, block_hash, energy_source
            nonce += 1

    def calculate_hash(self, block_data: str, nonce: int, energy_source: str) -> str:
        return hashlib.sha256(f"{block_data}{nonce}{energy_source}".encode()).hexdigest()

    def verify(self, transactions: List[Transaction], nonce: int, block_hash: str, energy_source: str) -> bool:
        block_data = json.dumps([tx.to_dict() for tx in transactions])
        return (
            self.calculate_hash(block_data, nonce, energy_source) == block_hash
            and block_hash.startswith("0" * self.difficulty)
            and energy_source in self.renewable_energy_sources
        )

    def adjust_difficulty(self):
        if len(self.block_times) >= self.adjustment_interval:
            average_block_time = sum(self.block_times) / len(self.block_times)
            if average_block_time < self.target_block_time:
                self.difficulty += 1
            elif average_block_time > self.target_block_time:
                self.difficulty = max(1, self.difficulty - 1)
            self.block_times = []

    def award_carbon_credits(self, miner_address: str, energy_source: str):
        base_credit = 1.0
        multiplier = {
            "solar": 1.2,
            "wind": 1.1,
            "hydro": 1.0,
            "geothermal": 1.3,
        }
        credits = base_credit * multiplier[energy_source]
        self.carbon_credits[miner_address] = self.carbon_credits.get(miner_address, 0) + credits
