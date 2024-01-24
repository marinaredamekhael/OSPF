from ospf_router import OSPFRouter


router_A = OSPFRouter("10", "192.168.1.1", 4444)
router_B = OSPFRouter("20","192.168.1.2", 5555)
router_C = OSPFRouter("30","192.168.1.3", 6666)
router_D = OSPFRouter("40","192.168.1.4", 7777)

router_A.add_connection(router_B, 1)
router_A.add_connection(router_C, 4)
router_A.add_connection(router_D, 6)
router_B.add_connection(router_A, 1)
router_B.add_connection(router_C, 5)
router_C.add_connection(router_A, 4)
router_C.add_connection(router_B, 5)
router_C.add_connection(router_D, 3)
router_D.add_connection(router_A, 6)
router_D.add_connection(router_C, 3)

# Simulating LSAs generation and propagation
router_A.generate_lsa()
router_B.generate_lsa()
router_C.generate_lsa()
router_D.generate_lsa()

# Displaying LSDB for Router A
print("LSDB of Router 10:")
for link_state_id, lsa in router_A.lsdb.items():
    print(f"Link State ID: {link_state_id} | LSA: {vars(lsa)}")

# Displaying LSDB for Router B
print("\nLSDB of Router 20:")
for link_state_id, lsa in router_B.lsdb.items():
    print(f"Link State ID: {link_state_id} | LSA: {vars(lsa)}")

# Displaying LSDB for Router C
print("\nLSDB of Router 30:")
for link_state_id, lsa in router_C.lsdb.items():
    print(f"Link State ID: {link_state_id} | LSA: {vars(lsa)}")

# Displaying LSDB for Router D
print("\nLSDB of Router 40:")
for link_state_id, lsa in router_D.lsdb.items():
    print(f"Link State ID: {link_state_id} | LSA: {vars(lsa)}")

forwarding_table_A, paths_A = router_A.build_forwarding_table()
print("\nForwarding Table for Router A:")
for dest_router_id, path_cost in forwarding_table_A.items():
    if dest_router_id != router_A.router_id:
        if isinstance(path_cost, int):
            path = paths_A[dest_router_id]
            print(f"Cost to reach Router {dest_router_id}: {path_cost}, the next stop is router: {path}")

forwarding_table_B, paths_B = router_B.build_forwarding_table()
print("\nForwarding Table for Router B:")
for dest_router_id, path_cost in forwarding_table_B.items():
    if dest_router_id != router_B.router_id:
        if isinstance(path_cost, int):
            path = paths_B[dest_router_id]
            print(f"Cost to reach Router {dest_router_id}: {path_cost}, the next stop is router: {path}")

forwarding_table_C, paths_C = router_C.build_forwarding_table()
print("\nForwarding Table for Router C:")
for dest_router_id, path_cost in forwarding_table_C.items():
    if dest_router_id != router_C.router_id:
        if isinstance(path_cost, int):
            path = paths_C[dest_router_id]
            print(f"Cost to reach Router {dest_router_id}: {path_cost}, the next stop is router: {path}")

forwarding_table_D, paths_D = router_D.build_forwarding_table()
print("\nForwarding Table for Router D:")
for dest_router_id, path_cost in forwarding_table_D.items():
    if dest_router_id != router_D.router_id:
        if isinstance(path_cost, int):
            path = paths_D[dest_router_id]
            print(f"Cost to reach Router {dest_router_id}: {path_cost}, the next stop is router:{path}")