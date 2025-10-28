from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ALTER COLUMN "comprobant_of_operation" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ALTER COLUMN "comprobant_of_operation" SET NOT NULL;"""


MODELS_STATE = (
    "eJztmm1vm0gQx7+K5VetlKtiX3yt7h0hROdr/CDHqU6qKrSGsb0KsHRZro0qf/furnkwjw"
    "GCg9PmnT07A7M/lv8sAz/6NjHB8t7NXKCIYeJMxP/+370ffQfZwH8UeJz1+sh143FhYGhl"
    "yRAS+kozWnmMIoPxkTWyPOAmEzyDYle4cKvjW5YwEoM7YmcTm3wHf/VBZ2QDbAuUD3z+ws"
    "3YMeE7eOFf915fY7DMRNrYFOeWdp09uNI2dti1dBRnW+kGsXzbiZ3dB7YlTuSNHSasG3DE"
    "bMA8yF+kF0w2NO1T5QZGfYhyNGODCWvkW+xgvgkI/endROutKbF7JmLIA3nyHCYGx8p58u"
    "w8OeGNOOkfw8HF+4sPf/518YG7yMQiy/vdfroxi32gJDJd9ndynJ9z7yGxxhyRTfw9iIos"
    "44BGPANaEc7QJeYZL6JyoKoyXXYGNAZo8Psji0/dIprPL/RP0eMpNlmNT8B3o3xqgs9G33"
    "ULnA3b8r+j8xJWn5SF+o+yeDM6fyuOTbhI7PVjGowM5VASJzIM3/YtiSBD9doiqGhZJuNS"
    "dNci8Hn5KurdpAHfEp5Xs7vLG603X2jq+HY8m4oD2g/eVyseFCZuwEzOeqEpNym82HYJZT"
    "pZ65GI18JcEN8Qd3tiMJ7MZz2y7kVZnR56l2IDmpPPD+8c/Fwdnzp4x7dXQHUKBvC8a5S6"
    "bGA7W4jmtKeUqMR2KVkhh8FJVL8wm0dWdiHkkiN0vcE4IP3EFd42dn5y0C0+Q2wW8L7iHv"
    "nA82JTpIULwza8Ez+ed4Vfa+qgZQlRlloevpLF+gi8skXaLbrh0dFRWAMFh5eiWk9g6bCu"
    "hfRKWyoncB8zbNwDq4cyEdM1R+123t1T7QFHPh7fljV55sV2zVWdL7viKlou6/vcZkESVc"
    "72lVDAG+cjPEjUY54b4vd8DtB012nJ7VHn6eQx78I1FFrjfQdF36JuVf7S4j/4PGG/XVWV"
    "W1W54iKbVYUW8C7lgTrg2lAWKnM9lMDHeUbFpwWki/BYHVBtWLSqUk3X6HywQh5WyLj/hq"
    "ipJ3RCjJAhSVki3+yQPbTTFuSgjWQipiISLxaKsiZ2Qk4qNLIDITz7pbrZwTU+QjO7mMEz"
    "d68fK0jFbdhsZOcN2YYl/wgN2cwWoPimj69F8q1Q8jpcBrHXHxdgFREvfBN18tegSGF3x5"
    "TEVCXKkcNsrSqWwkj8X1XwxamgCQxhq476xRGNVK+9HlvT5/CU6FVTvTLZ+711r+Wd5VF1"
    "7/ChJkf0Us88xYq3f4h4lbsXJ3eeCwaGnLutWO8OQrre5jXtmCUUb1BJ8QYlijc4z7x6Dy"
    "Dpdb9oSMd1TVglJt4QbZ/WieyoM+0dWuthJYrouFxLcaVPZjocVWA6HBUyFUO/cbVuubt2"
    "1GqtAMXGNq9QByOlNRrFPq8l+gWV6P+BejUbMgchHReQ6hRTolZN1cpkbZT5HI7fGjUgBu"
    "4vE+BRNjX8jAzyPnD993Y2LfoiJQpJgbxz+AQ/m9hgZz0Le+zLaWItoShmLZK2veAbqhDe"
    "m4nyX5qrejO7lBSIxzZUHkUe4LJe8W2/vOx+Ao+zKdo="
)
