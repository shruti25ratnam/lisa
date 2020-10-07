from lisa import LisaTestCase, TestCaseMetadata, TestSuiteMetadata
from lisa.testsuite import simple_requirement
from lisa.tools import Lscpu, Ntttcp


@TestSuiteMetadata(
    area="demo",
    category="demo",
    description="""
    this is an example test suite.
    It helps to understand how test cases works on multiple nodes
    """,
    tags=["demo", "multinode"],
    requirement=simple_requirement(min_count=2),
)
class MutipleNodesDemo(LisaTestCase):
    @TestCaseMetadata(
        description="""
        This test case send and receive data by ntttcp
        """,
        priority=1,
    )
    def os_info(self) -> None:
        self.log.info(f"node count: {len(self.environment.nodes)}")

        for node in self.environment.nodes.list():
            lscpu = node.tools[Lscpu]
            core_count = lscpu.get_core_count()
            self.log.info(f"index: {node.index}, core_count: {core_count}")

    @TestCaseMetadata(
        description="""
        this test case send and receive data by ntttcp
        """,
        priority=2,
    )
    def send_receive(self) -> None:
        self.log.info(f"node count: {len(self.environment.nodes)}")
        server_node = self.environment.nodes[0]
        client_node = self.environment.nodes[1]

        ntttcp_server = server_node.tools[Ntttcp]
        ntttcp_client = client_node.tools[Ntttcp]

        server_process = ntttcp_server.run_async("-P 1 -t 5 -e")
        client_result = ntttcp_client.run(
            f"-s {server_node.internal_address} -P 1 -n 1 -t 5 -W 1", no_info_log=False
        )
        server_result = server_process.wait_result(timeout=10)
        self.assertEqual(
            0,
            client_result.exit_code,
            f"client exit code [{client_result.exit_code}] should be 0.",
        )
        self.assertEqual(
            0,
            server_result.exit_code,
            f"server exit code [{server_result.exit_code}] should be 0.",
        )
